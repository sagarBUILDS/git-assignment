from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    Image as ReportImage,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).parent
EVIDENCE = ROOT / "evidence"
OUTPUT = ROOT / "assignment_report.pdf"


class PageNumberCanvas(Flowable):
    pass


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(18 * mm, 9 * mm, "Git & GitHub Workflow | Login System Test Cases")
    canvas.drawRightString(192 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def evidence_image(filename: str, title: str) -> Path:
    source = EVIDENCE / filename
    target = EVIDENCE / f"{source.stem}.png"
    text = source.read_text(encoding="utf-8-sig").strip()
    try:
        font = ImageFont.truetype("consola.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    lines = text.splitlines() or ["(no output)"]
    width = max(1000, max(len(line) for line in lines) * 13 + 80)
    height = len(lines) * 32 + 100
    image = Image.new("RGB", (width, height), "#0F172A")
    draw = ImageDraw.Draw(image)
    draw.text((35, 20), title, fill="#93C5FD", font=font)
    y = 68
    for line in lines:
        draw.text((35, y), line, fill="#E2E8F0", font=font)
        y += 32
    image.save(target)
    return target


def heading(text, styles):
    return Paragraph(text, styles["Heading2"])


def bullet(text, styles):
    return Paragraph(f"&bull; {text}", styles["BodyText"])


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="SubtitleCenter",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=13,
        leading=19,
        textColor=colors.HexColor("#475569"),
    )
)
styles["Heading1"].textColor = colors.HexColor("#1D4ED8")
styles["Heading2"].textColor = colors.HexColor("#0F766E")
styles["Heading2"].spaceBefore = 8
styles["Heading2"].spaceAfter = 6
styles["BodyText"].fontSize = 9.5
styles["BodyText"].leading = 14
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#475569"),
    )
)
styles.add(
    ParagraphStyle(
        name="AssignmentCode",
        parent=styles["BodyText"],
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
    )
)


history_png = evidence_image("commit-history.txt", "Commit history")
ignore_png = evidence_image("gitignore-verification.txt", ".gitignore verification")
undo_png = evidence_image("undo-reflog.txt", "Undo evidence (reflog)")
remote_png = evidence_image("remote.txt", "GitHub remote")

doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=17 * mm,
    bottomMargin=20 * mm,
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=footer)])

story = [
    Spacer(1, 25 * mm),
    Paragraph("Git & GitHub Workflow", styles["TitleCenter"]),
    Paragraph("University Assignment Portfolio", styles["SubtitleCenter"]),
    Spacer(1, 22 * mm),
    HRFlowable(width="80%", thickness=2, color=colors.HexColor("#2563EB")),
    Spacer(1, 15 * mm),
    Paragraph("<b>Student Name:</b> ______________________________", styles["BodyText"]),
    Spacer(1, 8 * mm),
    Paragraph("<b>Course:</b> ______________________________________", styles["BodyText"]),
    Spacer(1, 8 * mm),
    Paragraph("<b>Assignment Number:</b> ____________________________", styles["BodyText"]),
    Spacer(1, 25 * mm),
    Paragraph(
        "This portfolio documents the completed Git workflow, GitHub publication, and a professional Login System test-case suite.",
        styles["SubtitleCenter"],
    ),
    PageBreak(),
    Paragraph("Question 1 — Git & GitHub Workflow", styles["Heading1"]),
    Paragraph(
        "A new project named <b>GitAssignment</b> was initialized locally before any GitHub repository was created. "
        "The project contains index.html, about.html, README.md, .gitignore, git_commands.txt, and the final PDF.",
        styles["BodyText"],
    ),
    heading("Required workflow and merge", styles),
    bullet("Created the initial project and committed it as <b>Initial project setup</b>.", styles),
    bullet("Updated index.html and committed it as <b>Updated index page</b>.", styles),
    bullet("Created and checked out the <b>feature</b> branch, updated about.html, and committed <b>Added feature updates</b>.", styles),
    bullet("Checked out main and merged feature into main using a fast-forward merge.", styles),
    Spacer(1, 5),
    ReportImage(str(history_png), width=174 * mm, height=28 * mm),
    Spacer(1, 5),
    Paragraph(
        "The history evidence shows the three required commits and the merged feature content on main. "
        "The feature branch remains available locally.",
        styles["Small"],
    ),
    heading("Ignore rules", styles),
    Paragraph("The .gitignore file contains the following rules:", styles["BodyText"]),
    Paragraph("*.log<br/>temp/", styles["AssignmentCode"]),
    Paragraph(
        "A sample.log file and a file inside temp/ were created. Git verified both as ignored, so they do not appear in the working-tree status.",
        styles["BodyText"],
    ),
    ReportImage(str(ignore_png), width=174 * mm, height=22 * mm),
    PageBreak(),
    heading("Undo operation", styles),
    Paragraph(
        "A final demonstration commit named <b>Minor HTML improvement</b> was created and then undone using "
        "<b>git reset --soft HEAD~1</b>. The working files remained safe and README.md remained staged after the reset. "
        "The reflog below is direct repository evidence of the commit and reset.",
        styles["BodyText"],
    ),
    ReportImage(str(undo_png), width=174 * mm, height=56 * mm),
    heading("GitHub publication", styles),
    Paragraph(
        "A new public GitHub repository was created after the local workflow was complete. "
        "The local main branch was connected and pushed successfully.",
        styles["BodyText"],
    ),
    Paragraph(
        '<b>Repository URL:</b> <link href="https://github.com/sagarBUILDS/git-assignment">https://github.com/sagarBUILDS/git-assignment</link>',
        styles["BodyText"],
    ),
    ReportImage(str(remote_png), width=174 * mm, height=26 * mm),
    heading("All Git commands used", styles),
    Paragraph(
        "The complete command list and one-to-two-line explanations are provided in git_commands.txt in the repository. "
        "Representative commands are shown below.",
        styles["BodyText"],
    ),
    Paragraph(
        'git init -b main<br/>git add index.html about.html<br/>git commit -m "Initial project setup"<br/>'
        'git branch feature<br/>git switch feature<br/>git merge feature<br/>git log --oneline --graph --all<br/>'
        'git check-ignore -v sample.log temp\\temporary.txt<br/>git reset --soft HEAD~1<br/>git push -u origin main',
        styles["AssignmentCode"],
    ),
    PageBreak(),
    Paragraph("Question 2 — Login System Test Cases", styles["Heading1"]),
    Paragraph(
        "The following tests cover validation, successful authentication, credential errors, and account-lock behavior.",
        styles["BodyText"],
    ),
]

test_rows = [
    ["ID", "Test Scenario", "Input Data", "Expected Output"],
    ["TC-001", "Valid login", "student01 / Pass1234", "Login succeeds and redirects to the dashboard."],
    ["TC-002", "Invalid username", "unknown01 / Pass1234", "Display: Invalid username or password. No session is created."],
    ["TC-003", "Invalid password", "student01 / Wrong123", "Display: Invalid username or password. No session is created."],
    ["TC-004", "Both incorrect", "unknown01 / Wrong123", "Display: Invalid username or password. No session is created."],
    ["TC-005", "Empty username", "Username empty; Pass1234", "Display: Username cannot be empty. Login is not attempted."],
    ["TC-006", "Empty password", "student01; password empty", "Display: Password cannot be empty. Login is not attempted."],
    ["TC-007", "Both empty", "Username and password empty", "Display: Username cannot be empty. and Password cannot be empty. Login is not attempted."],
    ["TC-008", "Password < 6 characters", "student01 / Ab123 (5 chars)", "Display: Password must be at least 6 characters. Login is not attempted."],
    ["TC-009", "Password exactly 6 characters", "student01 / Ab1234 (6 chars)", "Validation passes; valid credentials log in and redirect to the dashboard."],
    ["TC-010", "Three failed attempts", "student01 / Wrong01, Wrong02, Wrong03", "After attempt 3 display: Account locked after 3 failed login attempts. Contact support. Further attempts are blocked."],
]

table_data = [[Paragraph(cell, styles["Small"]) for cell in row] for row in test_rows]
table = Table(table_data, colWidths=[15 * mm, 34 * mm, 44 * mm, 81 * mm], repeatRows=1)
table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.append(table)
story.append(Spacer(1, 8))
story.append(Paragraph("The same complete table is also available in test_cases.md.", styles["Small"]))

doc.build(story)
print(f"Generated {OUTPUT}")
