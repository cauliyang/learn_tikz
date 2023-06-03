from pathlib import Path


def get_code_url(path: Path):
    base_url = "https://github.com/cauliyang/learn_tikz/blob/main"
    return base_url + "/" + path.as_posix()


def create_table(texs):
    table = "|file name | code  | preview  |\n" "|---|---|---|\n"
    base_url = "https://github.com/cauliyang/learn_tikz/blob/main"
    for tex in texs:
        table += f"|{tex.name}|[code]({base_url}/{tex})|[preview]({base_url}/{tex.stem}.pdf)|\n"

    return table


def figure(path: Path):

    code = get_code_url(path)

    temp = R"""
    \section{{Example {}}}

    \begin{{figure}}[H]
        \centering
        \includestandalone[width=\textwidth]{{{}}}
        \caption{{{} \href{{{}}}{{{}}} }}
        \label{{fig:{}}}
    \end{{figure}}
    """.format

    caption = path.stem.replace("_", " ")

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
    add = True
    file_name = Path("main.tex")
    temp_name = Path("nmain.tex")

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

    with open(temp_name, "w") as f:
        f.writelines(content)

    try:
        with open(temp_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update tex error happend {e}")
        temp_name.unlink()
    else:
        file_name.unlink()
        temp_name.rename(file_name)


def update_readme(texs):
    table = create_table(texs)

    sep1 = "<!-- begin table -->\n"
    sep2 = "<!-- end table -->\n"

    content = []
    add = True

    file_name = Path("README.md")
    temp_name = Path("NREADME.md")

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
        with open(temp_name, "w") as f:
            f.writelines(content)
    except Exception as e:
        print(f"update readme error happend {e}")
        temp_name.unlink()
    else:
        file_name.unlink()
        temp_name.rename(file_name)


def main():
    texs = []
    for tex in Path(".").rglob("*tex"):
        texs.append(tex)
    update_readme(texs)
    update_latex(texs)


if __name__ == "__main__":
    main()
