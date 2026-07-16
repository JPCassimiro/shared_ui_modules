from PySide6.QtWidgets import QSlider, QProxyStyle, QStyle, QStyleOptionSlider, QStylePainter
from PySide6.QtCore import Qt, QRectF, QRect, QPoint
from PySide6.QtGui import QColor, QPalette

class duration_slider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setTickPosition(QSlider.TickPosition.TicksAbove)
        # self.setPageStep(1)
        self.setMinimumHeight(39)
    
    def paintEvent(self, ev):
        try:
            h_margin = -4
            v_margin = 1
            painter = QStylePainter(self)
            style_options = QStyleOptionSlider()
            self.initStyleOption(style_options)

            #handle rect, for margin
            handle_rect = self.style().subControlRect(QStyle.CC_Slider, style_options, QStyle.SC_SliderHandle, self)

            #draw slider
            style_options.subControls = QStyle.SC_SliderGroove
            painter.drawComplexControl(QStyle.CC_Slider, style_options)

            #draw handle
            style_options.subControls = QStyle.SC_SliderHandle
            painter.drawComplexControl(QStyle.CC_Slider, style_options)

            #tick marks
            interval = self.tickInterval()

            if interval == 0:
                interval = self.pageStep()

            if self.tickPosition() != QSlider.TickPosition.NoTicks:
                handle_width = handle_rect.width()
                val_range = self.maximum() - self.minimum()
                # draw_range = self.width() - handle_width - 2*h_margin
                draw_range = self.width() - handle_width
                f = draw_range / val_range

                for i in range(self.minimum()+1,self.maximum()):
                    tick_height = 5 
                    val_offset = i - self.minimum()#how far from slider start
                    # draw_offset = f*val_offset + handle_width//2 + h_margin
                    draw_offset = f*val_offset + handle_width//2
                    x = int(draw_offset)

                    painter.setPen(QColor(0,0,0))
                                        
                    if self.tickPosition() == QSlider.TickPosition.TicksBothSides or self.tickPosition() == QSlider.TickPosition.TicksAbove:
                        y = self.rect().top()
                        painter.drawLine(x,y,x,y + tick_height)
                        # text_y = y - tick_height//2
                        # painter.drawText(QPoint(x,text_y),numberStr)

                    if self.tickPosition() == QSlider.TickPosition.TicksBothSides or self.tickPosition() == QSlider.TickPosition.TicksBelow:
                        y = self.rect().bottom()
                        painter.drawLine(x,y,x,y - tick_height)

            if self.value() >= 1 and self.value() <= 8:
                #draw number bellow
                numberStr = str(self.value())
                number_x = handle_rect.center().x() - 2
                number_y = handle_rect.bottom() + painter.fontMetrics().ascent() + 2
                painter.drawText(QPoint(number_x,number_y),numberStr)
                    
            return super().paintEvent(ev)    
        except Exception as e:
            print(f"duration_slider error: {e}")