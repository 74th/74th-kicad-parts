"""
KiCad Edge.Cuts SVG をレーザーカット用に整形するスクリプト。

機能:
- g タグのグループ化を解除し、スタイルを子要素へ継承した上でフラット化する。
- 同じ端点を持つパスを結合して 1 つの連続したループにまとめる。

使い方:
	python convert_edge_cuts_svg.py input.svg [-o output.svg]

標準出力へ書き出す場合は -o を省略する。
"""

from __future__ import annotations

import argparse
import copy
import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


Point = Tuple[float, float]


@dataclass
class Segment:
	cmd: str
	start: Optional[Point]
	end: Point
	params: Tuple[float, ...] = ()


@dataclass
class PathData:
	segments: List[Segment]
	closed: bool
	attrib: Dict[str, str]

	@property
	def start(self) -> Point:
		return self.segments[0].end

	@property
	def end(self) -> Point:
		return self.segments[-1].end

	def to_element(self, ns: str) -> ET.Element:
		attrib = {k: v for k, v in self.attrib.items() if k != "d"}
		attrib["d"] = segments_to_d(self.segments, close=self.closed)
		return ET.Element(f"{ns}path", attrib)


def parse_style(style: Optional[str]) -> Dict[str, str]:
	if not style:
		return {}
	parts = [p.strip() for p in style.split(";") if p.strip()]
	result: Dict[str, str] = {}
	for part in parts:
		if ":" in part:
			key, value = part.split(":", 1)
			result[key.strip()] = value.strip()
	return result


def style_to_string(style: Dict[str, str]) -> str:
	return ";".join(f"{k}:{v}" for k, v in style.items())


def merge_styles(parent: Dict[str, str], child: Dict[str, str]) -> Dict[str, str]:
	merged = parent.copy()
	merged.update(child)
	return merged


def flatten_groups(root: ET.Element) -> List[ET.Element]:
	ns = extract_namespace(root)
	flattened: List[ET.Element] = []

	def walk(elem: ET.Element, inherited_style: Dict[str, str], inherited_transform: Optional[str]):
		current_style = merge_styles(inherited_style, parse_style(elem.attrib.get("style")))
		current_transform = elem.attrib.get("transform") or inherited_transform

		if elem.tag == f"{ns}g":
			for child in list(elem):
				walk(child, current_style, current_transform)
			return

		new_elem = copy.deepcopy(elem)
		if current_style:
			new_elem.attrib["style"] = style_to_string(current_style)
		if current_transform:
			if new_elem.attrib.get("transform"):
				new_elem.attrib["transform"] = f"{current_transform} {new_elem.attrib['transform']}"
			else:
				new_elem.attrib["transform"] = current_transform
		flattened.append(new_elem)

	for child in list(root):
		walk(child, {}, None)

	return flattened


def extract_namespace(elem: ET.Element) -> str:
	match = re.match(r"\{.*?\}", elem.tag)
	return match.group(0) if match else ""


def fmt_number(value: float) -> str:
	# 4 桁小数で末尾の 0 を除去する
	text = f"{value:.4f}"
	text = text.rstrip("0").rstrip(".")
	return text if text else "0"


def segments_to_d(segments: Sequence[Segment], close: bool) -> str:
	parts: List[str] = []
	for seg in segments:
		if seg.cmd == "M":
			x, y = seg.end
			parts.append(f"M {fmt_number(x)} {fmt_number(y)}")
		elif seg.cmd == "L":
			x, y = seg.end
			parts.append(f"L {fmt_number(x)} {fmt_number(y)}")
		elif seg.cmd == "A":
			rx, ry, rot, laf, sf, x, y = seg.params
			parts.append(
				f"A{fmt_number(rx)} {fmt_number(ry)} {fmt_number(rot)} {int(laf)} {int(sf)} {fmt_number(x)} {fmt_number(y)}"
			)
		else:
			raise ValueError(f"Unsupported command while writing: {seg.cmd}")

	if close:
		parts.append("Z")

	return "\n".join(parts)


def parse_path_data(d: str) -> Tuple[List[Segment], bool]:
	token_pattern = r"[A-Za-z]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"
	tokens = re.findall(token_pattern, d)
	if not tokens:
		raise ValueError("Empty path data")

	segments: List[Segment] = []
	current_cmd: Optional[str] = None
	idx = 0
	current_pos: Optional[Point] = None
	subpath_start: Optional[Point] = None
	closed = False

	def need_numbers(n: int) -> List[str]:
		nonlocal idx
		if idx + n > len(tokens):
			raise ValueError(f"Command '{current_cmd}' expects {n} numbers, but got fewer")
		vals = tokens[idx : idx + n]
		idx += n
		return vals

	while idx < len(tokens):
		token = tokens[idx]
		if re.fullmatch(r"[A-Za-z]", token):
			current_cmd = token
			idx += 1
			if current_cmd == "Z":
				if subpath_start is None:
					raise ValueError("'Z' without initial 'M'")
				current_pos = subpath_start
				closed = True
			continue

		if current_cmd is None:
			raise ValueError("Path data must start with a command")

		if current_cmd == "M":
			x, y = map(float, need_numbers(2))
			current_pos = (x, y)
			subpath_start = (x, y)
			segments.append(Segment("M", None, current_pos))
			# Additional pairs are treated as implicit 'L'
			while idx < len(tokens) and not re.fullmatch(r"[A-Za-z]", tokens[idx]):
				x, y = map(float, need_numbers(2))
				segments.append(Segment("L", current_pos, (x, y)))
				current_pos = (x, y)
		elif current_cmd == "L":
			while idx < len(tokens) and not re.fullmatch(r"[A-Za-z]", tokens[idx]):
				x, y = map(float, need_numbers(2))
				segments.append(Segment("L", current_pos, (x, y)))
				current_pos = (x, y)
		elif current_cmd == "A":
			while idx < len(tokens) and not re.fullmatch(r"[A-Za-z]", tokens[idx]):
				rx, ry, rot, laf, sf, x, y = map(float, need_numbers(7))
				segments.append(Segment("A", current_pos, (x, y), (rx, ry, rot, laf, sf, x, y)))
				current_pos = (x, y)
		else:
			raise ValueError(f"Unsupported command: {current_cmd}")

	if not segments:
		raise ValueError("No segments parsed")

	return segments, closed


def points_close(a: Point, b: Point, tol: float = 1e-4) -> bool:
	return math.isclose(a[0], b[0], abs_tol=tol) and math.isclose(a[1], b[1], abs_tol=tol)


def reverse_segments(segments: Sequence[Segment]) -> List[Segment]:
	if not segments:
		return []

	reversed_segments: List[Segment] = []
	current_pos = segments[-1].end
	reversed_segments.append(Segment("M", None, current_pos))

	for seg in reversed(segments[1:]):
		if seg.cmd == "L":
			new_end = seg.start  # type: ignore[arg-type]
			reversed_segments.append(Segment("L", current_pos, new_end))
			current_pos = new_end
		elif seg.cmd == "A":
			rx, ry, rot, laf, sf, x, y = seg.params
			new_end = seg.start  # type: ignore[arg-type]
			reversed_segments.append(
				Segment("A", current_pos, new_end, (rx, ry, rot, laf, 1 - sf, new_end[0], new_end[1]))
			)
			current_pos = new_end
		else:
			raise ValueError(f"Unsupported command for reversing: {seg.cmd}")

	return reversed_segments


def merge_open_paths(paths: List[PathData]) -> List[PathData]:
	merged: List[PathData] = []
	remaining = paths.copy()

	while remaining:
		current = remaining.pop(0)
		segments = list(current.segments)
		start_pt = current.start
		end_pt = current.end

		changed = True
		while changed:
			changed = False
			for idx, candidate in enumerate(remaining):
				if points_close(candidate.start, end_pt):
					segments.extend(candidate.segments[1:])
					end_pt = candidate.end
					remaining.pop(idx)
					changed = True
					break
				if points_close(candidate.end, end_pt):
					rev = reverse_segments(candidate.segments)
					segments.extend(rev[1:])
					end_pt = rev[-1].end
					remaining.pop(idx)
					changed = True
					break
				if points_close(candidate.end, start_pt):
					segments = candidate.segments + segments[1:]
					start_pt = candidate.start
					remaining.pop(idx)
					changed = True
					break
				if points_close(candidate.start, start_pt):
					rev = reverse_segments(candidate.segments)
					segments = rev + segments[1:]
					start_pt = rev[0].end
					remaining.pop(idx)
					changed = True
					break

		close_loop = points_close(start_pt, end_pt)
		if not close_loop:
			# 明示的にループにする
			segments.append(Segment("L", end_pt, start_pt))
			close_loop = True

		merged.append(PathData(segments=segments, closed=close_loop, attrib=current.attrib))

	return merged


def parse_paths(flattened: Iterable[ET.Element], ns: str) -> Tuple[List[PathData], List[ET.Element]]:
	paths: List[PathData] = []
	others: List[ET.Element] = []

	for elem in flattened:
		if elem.tag == f"{ns}path":
			segments, closed = parse_path_data(elem.attrib.get("d", ""))
			paths.append(PathData(segments=segments, closed=closed, attrib=elem.attrib))
		else:
			others.append(elem)

	return paths, others


def build_svg(tree: ET.ElementTree) -> ET.ElementTree:
	root = tree.getroot()
	ns = extract_namespace(root)

	flattened = flatten_groups(root)
	path_data, others = parse_paths(flattened, ns)

	closed_paths = [p for p in path_data if p.closed]
	open_paths = [p for p in path_data if not p.closed]

	merged_open = merge_open_paths(open_paths)

	new_children: List[ET.Element] = []
	new_children.extend(others)
	for pdata in closed_paths + merged_open:
		new_children.append(pdata.to_element(ns))

	root[:] = new_children
	return tree


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="KiCad Edge.Cuts SVG converter")
	parser.add_argument("input", help="入力 SVG ファイル")
	parser.add_argument("-o", "--output", help="出力 SVG ファイル。未指定なら標準出力に書き出す")
	return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
	args = parse_args(sys.argv[1:] if argv is None else argv)
	tree = ET.parse(args.input)
	converted = build_svg(tree)

	if hasattr(ET, "indent"):
		ET.indent(converted, space="  ")  # type: ignore[attr-defined]

	if args.output:
		converted.write(args.output, encoding="utf-8", xml_declaration=True)
	else:
		converted.write(sys.stdout.buffer, encoding="utf-8", xml_declaration=True)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
