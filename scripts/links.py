from os import writev
from pathlib import Path


def write_table(texs):
    table = "|file name | code  | preview  |\n" "|---|---|---|\n"
    base_url = "https://github.com/cauliyang/learn_tikz/blob/main"
    for tex in texs:
        table += f"|{tex.name}|[code]({base_url}/{tex})|[preview]({base_url}/{tex.name}.pdf)|\n"

    return table


def main():
    texs = []
    for tex in Path(".").rglob("*tex"):
        texs.append(tex)

    tex_table = write_table(texs)

    sep1 = "<!-- begin table -->\n"
    sep2 = "<!-- end table -->\n"
    content = []
    add = True

    with open("README.md") as f:
        for line in f:
            if line == sep1:
                add = False
                content.append(line)
                content.append(tex_table)

            if line == sep2:
                add = True

            if add:
                content.append(line)

    with open("README.md", "w") as f:
        f.writelines(content)


if __name__ == "__main__":
    main()
