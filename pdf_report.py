from fpdf import FPDF
from PIL import Image

class PDF(FPDF):
    proj_title = ''

    def header(self):
        self.set_font('Arial', '', 14)
        self.image('./images/HTW_logo.jpeg', 5, 5, 0, 15)
        title = f'Project Title: {self.proj_title}'
        title_width = self.get_string_width(title)
        title_x_pos = (self.w - title_width)/2
        self.set_x(title_x_pos)
        self.set_text_color(250, 0, 0)
        self.cell(0,0,f'{title}', 'C')
        img_1 = Image.open('./images/FMER_logo.jpeg')
        original_width_1, original_height_1 = img_1.size
        image_width_1 = original_width_1 * 15 / original_height_1      
        img2 = Image.open('./images/MEWAC_logo.jpeg')  
        original_width_2, original_height_2 = img2.size
        image_width_2 = original_width_2 * 15 / original_height_2
        self.image('./images/FMER_logo.jpeg', self.w - image_width_2 - image_width_1 - 10, 5, w=0, h=15)
        self.image('./images/MEWAC_logo.jpeg', self.w - image_width_2 - 5, 5, w=0, h=15)
        self.set_x(5)
        self.set_y(22)
        self.set_font('Arial', 'I', 12)
        self.cell(0, 5, 'RBFSim Tool: https://rbf-sim.streamlit.app/', link="https://rbfsim-dup.streamlit.app/", ln=2)
        original_x = self.get_x()
        original_y = self.get_y()
        self.set_xy(1, self.w)
        self.rotate(90)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(250, 0, 0)
        self.cell(self.w, 5, 'The authors of RBFSim tool are not liable for the results generated.', 0, 1, 'C')
        self.rotate(0)
        self.set_xy(original_x, original_y)
        self.set_margins(10, 10, 10)

    
    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 5,'BMBF Project: Feasibility of Managed Aquifer Recharge for safe and sustainable water supply (FEMAR, Nr: FKZ 02WME1612A-C) \nContact: Prof. Thomas Grischek, HTW Dresden, Friedrich-List-Platz 1, D-01069 Dresden Email: thomas.grischek@htw-dresden.de', align = 'C')
        # self.cell(0, 5, 'Page %s' % self.page_no(), 0, 0, 'C')