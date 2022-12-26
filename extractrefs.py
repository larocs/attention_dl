from refextract import extract_references_from_file, extract_references_from_url
import sys
import json


def main():
    if len(sys.argv) < 2:
        print('usage: extractrefs <pdf_path> [dst_path]')
        return

    pdf_path = sys.argv[1]
    assert pdf_path.endswith('.pdf')
    dst_path = \
        sys.argv[2] if len(sys.argv) > 2 else pdf_path.replace('.pdf', '.json')

    if pdf_path.startswith('http://') or pdf_path.startswith('https://'):
        # refs = refextract.extract_references_from_url(pdf_path)
        refs = extract_references_from_url(pdf_path)
    else:
        # refs = refextract.extract_references_from_file(pdf_path)
        refs = extract_references_from_file(pdf_path)

    with open(dst_path, 'w') as f:
        json.dump(refs, f, indent=4)
    print('saved refs to %s' % dst_path)

if __name__ == '__main__':
    main()
