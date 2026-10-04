# python-hwpx 6.x API 치트시트

스크립트로 안 되는 작업(이미지·머리말·페이지설정·서식)을 직접 코딩할 때 참조.
버전 6.3 기준 실측. 모든 예시는 `~/hwpx-env/bin/python`으로 실행.

## 열기·저장

```python
from hwpx.document import HwpxDocument

d = HwpxDocument.new()              # 빈 문서
d = HwpxDocument.open("f.hwpx")     # 기존 문서

d.save_to_path("out.hwpx")          # ⚠️ save() 없음
d.save_to_stream(fp)
data = d.to_bytes()
```

## 읽기

```python
d.text.markdown()      # 표 포함 마크다운 (메서드 — 프로퍼티 아님)
d.text.plain()
d.text.html()
d.validate()           # ValidationReport(issues=()) 면 스키마 OK
len(d.sections); list(d.paragraphs); list(d.tables)
d.media.images         # 이미지 목록
d.fields.all()         # 양식 필드
```

## 쓰기 — 본문

```python
d.add_heading("제목", level=1)
d.add_paragraph("문단", para_pr_id_ref=None, style=None)
d.add_hyperlink("https://…", "표시문구")
d.add_image(image_data: bytes, image_format: str)     # 바이너리 등록 → item_id
d.add_picture(image_data, image_format, width=…, height=…)   # 본문 배치
d.add_footnote(...); d.add_endnote(...); d.add_memo(...)
d.add_equation(...)
```

## 쓰기 — 표

```python
t = d.add_table(rows=3, cols=2, width=None, height=None)
t.set_cell_text(r, c, "값")          # 0-based
t.cell(r, c).text                    # 읽기
t.row_count; t.column_count; t.get_cell_map(); t.iter_grid()
t.merge_cells(...); t.split_merged_cell(...)
t.set_cell_shading(...); t.set_cell_border_fill(...)
t.set_column_widths([...]); t.equalize_column_widths()
```

### 라벨 기반 (양식 채우기에 최적)

```python
d.tables.find_cell_by_label("상      호")
# → {'matches': [{'table_index': 5,
#                 'label_cell': {'row':1,'col':0,'text':'상      호'},
#                 'target_cell': {'row':1,'col':1,'text':' OOO '}}], 'count': 1}

d.tables.fill_by_path({"상      호>right": "주식회사 예시",
                       "대  표  자>right": "홍길동"})
# → {'applied_count': 2, 'failed_count': 0, 'failed': []}
```
- 방향: `right` `left` `below` `above`, `>`로 체이닝 (`"라벨>right>below"`)
- **매칭은 부분문자열이지만 내부 공백을 뭉개지 않는다** — `'상호'`는 0건, `'상      호'`는 1건.
  라벨은 `hwpx_read.py --labels` 출력을 그대로 복사할 것

## 치환

```python
d.text.replace("찾을값", "바꿀값", limit=None, text_color=None, char_pr_id_ref=None)
```
🚨 **본문 문단만 바뀐다. 표 셀은 안 닿는다.** 표는 직접 순회해 `set_cell_text`.
(`hwpx_fill.py`가 이미 이 분기를 처리함)

## 페이지·머리말

```python
d.set_page_setup(paper_size="A4", orientation=…, margins_mm={...})
d.set_page_margins(left=…, right=…, top=…, bottom=…, header=…, footer=…)
d.set_header_text("머리말", page_type="BOTH")
d.set_footer_text("꼬리말"); d.set_page_number(...)
d.set_columns(col_count=2)
d.set_paragraph_format(paragraph_index=3, alignment="CENTER", line_spacing_percent=160)
```

## 6.0 이동 목록 (7.0에서 구 API 제거)

| 구 API | 신 API |
|---|---|
| `doc.save()` | `doc.save_to_path()` |
| `doc.export_markdown()` | `doc.text.markdown()` |
| `doc.list_form_fields()` | `doc.fields.all()` |
| `doc.list_images()` | `doc.media.images` |
| `doc.find_cell_by_label()` | `doc.tables.find_cell_by_label()` |
| `doc.fill_by_path()` | `doc.tables.fill_by_path()` |

DeprecationWarning이 뜨면 위 표로 교체. 경고 무시하고 두면 7.0에서 깨짐.

## 실측 확인된 성질

- **무손실 왕복**: 2.8MB 실제 관공서 양식(표 32·문단 314·BinData 22MB) 열고 저장 →
  ZIP 엔트리 46개 전량 보존, BinData 바이트 동일. 파일 크기 감소는 재압축일 뿐
- 표 셀의 문단은 `d.paragraphs`에 포함되지 않는다 (본문 문단과 분리 집계)
- 스크립트 파일명을 `inspect.py`로 두면 stdlib `inspect` 섀도잉 → 순환 임포트 크래시
