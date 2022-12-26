def dict2ris(metadata):
    fields = []
    fields.append(f"TI  - {metadata['title']}")
    fields.append(f"AB  - {metadata['abstract']}")
    for author in metadata["authors"]:
        fields.append(f"AU  - {author}")
    url = f"https://arxiv.org/pdf/{metadata['arxiv_id']}.pdf"
    fields.append(f"UR  - {url}")
    ris = "TY  - GEN\n" + "\n".join(fields) + "\nER  - "
    return ris


if __name__ == "__main__":
    from glob import glob
    import json

    filenames = glob("arxiv_papers_infos/*.json")
    all_ris = ""

    for filename in filenames:
        with open(filename, "r") as f:
            content = json.load(f)["result"]
            ris = dict2ris(content)
            all_ris += ris + "\n"

    with open("arxiv_papers.ris", "w") as f:
        f.write(all_ris)
