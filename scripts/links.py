from pathlib import Path


preview_base_url = "https://github.com/cauliyang/learn_tikz/blob/main/gallery"


def get_code_url(path: Path):
    return Path(preview_base_url).parent / "source" / path.as_posix()


def create_table(texs):
    table = "|file name | code  | preview  |\n" "|---|---|---|\n"
    for tex in texs:
        table += f"|{tex.name}|[code]({get_code_url(tex)})|[preview]({preview_base_url}/{tex.stem}.pdf)|\n"

    return table


def figure(path: Path):
    code = get_code_url(path).as_posix()
    code.replace("_", "\_")
    caption = path.stem.replace("_", " ")

    temp = R"""
\section{{Case {}}}

\begin{{figure}}[H]
    \centering
    \includestandalone[width=\textwidth]{{{}}}
    \caption{{{} \href{{{}}}{{{}}} }}
    \label{{fig:{}}}
\end{{figure}}
    """.format

    return temp(caption, path.stem, caption, code, "code", caption)


def create_tex(texs):
    res = []
    for tex in texs:
        if tex.name not in ["main.tex", "nmain.tex"]:
            res.append(figure(tex))

    return "".join(res)


def update_latex(texs):
    figures = create_tex(texs)

    start_sep = "% <!-- begin content -->\n"
    end_sep = "% <!-- end content -->\n"

    content = []

    file_name = Path("main.tex")
    add = True
    with open(file_name) as f:
        for line in f:
            if line.lstrip() == start_sep:
                add = False
                line = line.lstrip()
                content.append(line)
                content.append(figures)

            if line.lstrip() == end_sep:
                add = True
                line = line.lstrip()

            if add:
                content.append(line)
    try:
        with open(file_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update tex error happend {e}")


def update_readme(texs):
    table = create_table(texs)

    start_sep = "<!-- begin table -->\n"
    end_sep = "<!-- end table -->\n"

    content = []
    file_name = Path("README.md")

    add = True
    with open(file_name) as f:
        for line in f:
            if line == start_sep:
                add = False
                content.append(line)
                content.append(table)

            if line == end_sep:
                add = True

            if add:
                content.append(line)

    try:
        with open(file_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update readme error happend {e}")


def main():
    texs = []
    ignore = ["arrow.tex"]
    for tex in Path(".").rglob("*tex"):
        if tex.name not in ignore:
            texs.append(tex)
    update_readme(texs)
    update_latex(texs)


if __name__ == "__main__":
    main()
