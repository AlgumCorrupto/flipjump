from manim import *
import re

class Scn(Scene):
    def construct(self):
        title = Text("FlipJump")
        title.to_edge(UL)
        self.camera.background_color = ManimColor.from_hex('#0d1117')
        self.play(Write(title))
        self.wait()
        self.parse("sample.fj")

    def fadeAll(self): 
        self.play(*[FadeOut(mob)for mob in self.mobjects])

    def parse(self, codefile: str):
        # prologue ##############################
        # create code snippet
        codegui = Code(
            codefile,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color="WHITE",
            background="window",
            insert_line_no=False,
            style=Code.styles_list[15],
            language="cpp"
        )
        codegui.to_edge(UP)
        codegui.shift(DOWN)
        self.play(FadeIn(codegui))


        programPointer = Arrow(start=LEFT, end=RIGHT, color=BLUE)
        programPointer.next_to(codegui.code[0], LEFT)
        code = open(codefile).readlines()
        memsize = int(re.findall("memsize ([0-9]+)", code[0])[0])
        # create memcells template
        memcellrect = Rectangle(WHITE, height=0.7, width=0.7)
        memcellnumber = DecimalNumber(0, num_decimal_places=0, unit_buff_per_font_unit=0.003)
        memcellnumber.move_to(memcellrect.get_center())
        memcell = VGroup(memcellnumber, memcellrect)
        ramtemp = []
        for i in range(memsize):
            buffcell = memcell.copy()
            if i != 0:
                buffcell.next_to(ramtemp[i-1], buff=0)
            ramtemp.append(buffcell)
        ramdisplay = VGroup(*ramtemp)
        ramdisplay.shift(-ramdisplay.get_center())
        ramdisplay.to_edge(DOWN)
        self.play(FadeIn(programPointer, ramdisplay))
        self.wait()
        mempointer = 0
        currMem = ramdisplay[mempointer]
        pointerArrow = Arrow(start=UP, end=DOWN, color=RED)
        pointerArrow.next_to(currMem, UP)
        currMemRect = memcellrect.copy()
        currMemRect.move_to(currMem.get_center())
        currMemRect.set_color(GREEN_B)

        self.play(FadeIn(pointerArrow, currMemRect))
        # Do the actual eval of the instructions ############################
        for i in range(1, len(code)):
            if code[i] == "\n":
                continue
            flip, jump = re.findall(r"(\-*[0-9]+) +(\-*[0-9]+)", code[i])[0]
            currMem = ramdisplay[mempointer + int(flip)]
            self.play(
                pointerArrow.animate.next_to(ramdisplay[mempointer], UP)
            )
            self.play(
                programPointer.animate.next_to(codegui.code[i], LEFT),
            )
            direction = 1 if currMem.get_edge_center(UP)[0] - pointerArrow.get_tip().get_center()[0] >= 0 else -1
            offset = CurvedArrow(
                start_point=pointerArrow.get_tip().get_center(),
                end_point=currMem.get_edge_center(UP),
                color=GREEN,
                angle=-PI/4 * direction
            )
            self.play(
                Write(offset),
                currMemRect.animate.move_to(currMem[1].get_center())
            )
            self.play(
                currMem[0].animate.set_value(not currMem[0].get_value())
            )
            self.wait()
            self.play(Unwrite(offset))
            mempointer = int(jump)
        self.play(
            pointerArrow.animate.next_to(ramdisplay[mempointer], UP)
        )
        self.wait()
        self.clear()
