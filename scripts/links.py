from pathlib import Path


preview_base_url = "https://github.com/cauliyang/learn_tikz/blob/main/gallery"


def get_code_url(path: Path):
    return Path(preview_base_url).parent / path.as_posix()


def create_table(texs):
    table = "|file name | code  | preview  |\n" "|---|---|---|\n"
    for tex in texs:
        table += f"|{tex.name}|[code]({preview_base_url}/{tex})|[preview]({preview_base_url}/{tex.stem}.pdf)|\n"

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

    sep1 = "% <!-- begin content -->\n"
    sep2 = "% <!-- end content -->\n"

    content = []
    file_name = Path("template/main.tex")

    result_name = Path("main.tex")
    add = True

    with open(file_name) as f:
        for line in f:
            if line == sep1:
                add = False
                content.append(line)
                content.append(figures)

            if line == sep2:
                add = True

            if add:
                content.append(line)
    try:
        with open(result_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update tex error happend {e}")


def update_readme(texs):
    table = create_table(texs)

    sep1 = "<!-- begin table -->\n"
    sep2 = "<!-- end table -->\n"

    content = []
    add = True

    file_name = Path("template/README.md")
    res_name = Path("README.md")

    with open(file_name) as f:
        for line in f:
            if line == sep1:
                add = False
                content.append(line)
                content.append(table)

            if line == sep2:
                add = True

            if add:
                content.append(line)

    try:
        with open(res_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update readme error happend {e}")


def main():
    texs = []
    for tex in Path(".").rglob("*tex"):
        texs.append(tex)
    update_readme(texs)
    update_latex(texs)


if __name__ == "__main__":
    main()
