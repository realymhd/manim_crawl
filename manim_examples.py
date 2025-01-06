from manim import *

"""
Collection of Manim animation examples organized by categories
"""

class BasicAnimations(Scene):
    def construct(self):
        # Create animations
        square = Square()
        circle = Circle()
        triangle = Triangle()
        text = Text("Create")
        
        self.play(Create(square))
        self.play(Write(text))
        self.play(DrawBorderThenFill(triangle))
        self.wait()
        self.clear()

        # Different lag_ratios
        dots = VGroup(*[Dot() for _ in range(4)]).arrange(RIGHT)
        self.play(Create(dots), lag_ratio=0.5)
        self.play(dots.animate.shift(UP), lag_ratio=1.0)

class TransformAndMoving(Scene):
    def construct(self):
        # Transform and MoveToTarget
        square = Square()
        circle = Circle()
        circle.generate_target()
        circle.target.shift(RIGHT * 2)
        
        self.play(Transform(square, circle))
        self.play(MoveToTarget(circle))
        self.wait()
        self.clear()
        
        # Rotate and MoveAlongPath
        dot = Dot()
        path = Circle(radius=2)
        self.play(Rotate(dot, angle=TAU, about_point=ORIGIN))
        self.play(MoveAlongPath(dot, path))

class FadingAndGrowing(Scene):
    def construct(self):
        # Fading examples
        text1 = Text("Fade In")
        text2 = Text("Fade Out")
        self.play(FadeIn(text1))
        self.play(FadeTransform(text1, text2))
        self.play(FadeOut(text2))
        self.wait()
        self.clear()
        
        # Growing examples
        circle = Circle()
        self.play(GrowFromCenter(circle))
        self.play(circle.animate.scale(0.3))
        self.play(ShrinkToCenter(circle))

class IndicationAndEffects(Scene):
    def construct(self):
        # Different indications
        text = Text("Important!")
        circle = Circle()
        dot = Dot()
        
        self.play(Write(text))
        self.play(Indicate(text))
        self.play(Circumscribe(text))
        self.play(FocusOn(dot))
        self.play(ApplyWave(circle))
        self.wait()