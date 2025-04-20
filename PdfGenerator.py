from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont



class PDFGeneratorReportLab:
    def __init__(self, data: str, idx=1, filename="output_reportlab.pdf"):
        self.idx=idx
        self.data = data
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        self.y = self.height - inch  # Start 1 inch from top
        
        

    def draw_text(self, text: str, font: str = "Helvetica", size: int = 12, spacing: int = 18, line_gap: int = 0.5, para_gap: int = 0.1):
        """Draw formatted text to the PDF, preserving new lines and text formatting"""
        if not text:
            return
        self.canvas.setFont(font, size)
        
        # lines = self.wrap_text(text, 90)  # Wrapping text to 90 chars
        # for line in lines:
        #     if line.strip() == "":
        #         self.y -= para_gap  # Empty line = paragraph break
        #     else:
        #         wrapped_lines = self.wrap_text(line.strip(), 90)
        #         for wrapped_line in wrapped_lines:
        #             self.canvas.drawString(70, self.y, wrapped_line)
        #             self.y -= (spacing+line_gap)
    
        #             self.check_page_end()

        lines = text.splitlines()
        for line in lines:
            if line.strip() == "":
                self.y -= para_gap  # Empty line = paragraph break
            else:
                wrapped_lines = self.wrap_text(line.strip(), 90)
                for wrapped_line in wrapped_lines:
                    self.canvas.drawString(70, self.y, wrapped_line)
                    self.y -= spacing
                    self.check_page_end()
            self.y -= para_gap
            self.y -= 10
            

    def wrap_text(self, text, max_chars):
        """Wrap text to fit within the specified max character width"""
        if not isinstance(text, str):
            text = str(text)
        # Split the text by lines
        lines = text.split('\n')
        wrapped_lines = []
        for line in lines:
            wrapped_lines.extend([line[i:i + max_chars] for i in range(0, len(line), max_chars)])
        return wrapped_lines

    def check_page_end(self):
        """Check if the content goes past the page end and create a new page if necessary"""
        if self.y < 100:
            self.canvas.showPage()
            self.canvas.setFont("Helvetica", 12)
            self.y = self.height - inch  # Reset Y position

    def generate(self):
        """Generate the PDF from the provided string data"""
        self.canvas.setFont("Helvetica-Bold", 16)
        self.canvas.drawCentredString(self.width / 2, self.y, "Lecture No. "+str(self.idx))
        self.y -= 30
        # self.canvas.drawCentredString(self.width / 2, self.y, "------------------------------------")

        # Draw the main content
        summary = self.data
        if summary:
            self.draw_text(summary)

        self.canvas.save()
        

# --- Usage Example ---

# Example formatted data (with newlines and spacing)
formatted_data = """
In this video, the speaker demonstrates how to give referencing the decimal degree restore data using a geographic information system (GIS) tool. The steps include loading the data, marking the reference points, entering the coordinates, and creating a new geographic reference.

Key points:
- To give referencing the decimal degree restore data, the first step is to load the data into the GIS tool.
- Reference points are marked at the furthest points in the image by clicking and adding points while scrolling and dragging.
- The coordinates for each point are then entered, including the east and north values.
- After marking three points, it is recommended to add a fourth point for confirmation of the location of the entire image.
- Once the referencing is complete, a new geographic reference is created, saved, and loaded into the project.
- The reference can be confirmed by comparing it with previous data.

MCQ:
1. How many reference points should be marked in the image?
   a) 2
   b) 3
   c) 4
   Answer: c) 4
2. What are the coordinates entered for each reference point?
   a) East
   b) North
   c) South
   Answer: a) East and b) North

Short questions:
1. What are the key steps involved in giving referencing to the decimal degree restore data?
   Answer: Loading the data, marking reference points, entering coordinates, and creating a new geographic reference.
2. Why is it recommended to add a fourth reference point?
   Answer: To confirm the location of the entire image.
"""

# Create PDF
pdf = PDFGeneratorReportLab(formatted_data, "output.pdf")
pdf.generate()
