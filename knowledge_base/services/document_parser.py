import io
import zipfile
import xml.etree.ElementTree as ET

class DocumentParseError(Exception):
    pass


def _extract_txt(file_obj):
    data = file_obj.read()
    for encoding in ('utf-8', 'gbk', 'gb2312'):
        try:
            return data.decode(encoding)
        except Exception:
            continue
    raise DocumentParseError('TXT 编码无法识别，请使用 UTF-8/GBK 编码')


def _extract_docx(file_obj):
    raw = file_obj.read()
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            xml_content = zf.read('word/document.xml')
        root = ET.fromstring(xml_content)
        texts = []
        for node in root.iter():
            if node.tag.endswith('}t') and node.text:
                texts.append(node.text)
        return '\n'.join(texts).strip()
    except Exception as e:
        raise DocumentParseError(f'DOCX 解析失败: {e}') from e


def _extract_pdf(file_obj):
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise DocumentParseError(
            '缺少 pypdf 依赖，请先执行 pip install -r requirements.txt'
        ) from e

    try:
        reader = PdfReader(file_obj)
        texts = []
        for page in reader.pages:
            text = page.extract_text() or ''
            if text.strip():
                texts.append(text.strip())
        return '\n\n'.join(texts).strip()
    except Exception as e:
        raise DocumentParseError(f'PDF 解析失败: {e}') from e


def extract_text_from_file(uploaded_file):
    name = (uploaded_file.name or '').lower()
    if name.endswith('.txt'):
        return _extract_txt(uploaded_file)
    if name.endswith('.docx'):
        return _extract_docx(uploaded_file)
    if name.endswith('.pdf'):
        return _extract_pdf(uploaded_file)
    raise DocumentParseError('仅支持 pdf/docx/txt 文件')

