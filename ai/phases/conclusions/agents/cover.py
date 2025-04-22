def generate_cover() -> str:
    title = "Investigación generada por IA Generativa"
    author = "Urolobot"
    institution = "Universidad Complutense de Madrid"
    
    return f"""
\\begin{{titlepage}}
\\centering
\\vspace*{{4cm}}

{{\\Huge \\textbf{{{title}}} \\\\[1.5cm]}}

{{\\Large {author} \\\\[0.5cm]}}
{{\\large {institution} \\\\[0.5cm]}}

\\vfill
\\large \\today

\\end{{titlepage}}
"""
