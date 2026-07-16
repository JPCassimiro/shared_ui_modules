from PySide6.QtWidgets import QSlider, QProxyStyle, QStyle, QStyleOptionSlider, QStylePainter
from PySide6.QtCore import Qt, QRectF, QRect, QPoint
from PySide6.QtGui import QColor, QPalette, QPainterPath

#when recompiled, this class needs to be imported to config_widget_ui
#allows the slider to be clicked, not dragged
class pressure_slider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def mousePressEvent(self, event):
        super(pressure_slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            length = self.height()
            click_pos = event.position().y()
            ratio = (length - click_pos) / length
            value = ratio * self.maximum()
            self.setValue(int(value))
            event.accept()
        else:
            return super().mousePressEvent(event)
    
    def paintEvent(self, ev):
        try:
            painter = QStylePainter(self)
            style_options = QStyleOptionSlider()
            self.initStyleOption(style_options)

            #draw slider groove
            style_options.subControls = QStyle.SC_SliderGroove
            painter.drawComplexControl(QStyle.CC_Slider, style_options)

            groove_rect = self.style().subControlRect(QStyle.CC_Slider,style_options,QStyle.SC_SliderGroove,self)
            
            #draw handle
            style_options.subControls = QStyle.SC_SliderHandle
            painter.drawComplexControl(QStyle.CC_Slider, style_options)

            handle_rect = self.style().subControlRect(QStyle.CC_Slider, style_options, QStyle.SC_SliderHandle, self)

            if self.value() > 0:
                black = QColor("black")
                painter.setBrush(black)
                full_subpage = QRect(groove_rect.left(), handle_rect.center().y(), groove_rect.width(), groove_rect.bottom() - handle_rect.center().y() + 1)

                path = QPainterPath()                
                path.setFillRule(Qt.WindingFill)
                # painter.fillPath(path, QColor("black"))
                
                r = groove_rect.width() / 2
                d = r*2
                h = full_subpage.height()

                if self.value() == 1:
                    painter.drawEllipse(full_subpage.left() + (full_subpage.width()*0.5)*0.6, full_subpage.bottom() - h, d - full_subpage.width()*0.5, h)
                elif self.value()/self.maximum() < 0.04 and self.value() != 1:
                    painter.drawEllipse(full_subpage.left() + (full_subpage.width()*0.4)*0.5, full_subpage.bottom() - h, d - full_subpage.width()*0.4, h)
                elif self.value()/self.maximum() <= 0.045 and self.value()/self.maximum() >= 0.04:
                    painter.drawEllipse(full_subpage.left() + (full_subpage.width()*0.3)*0.6, full_subpage.bottom() - h, d - full_subpage.width()*0.3, h)
                elif self.value()/self.maximum() <= 0.05:
                    painter.drawEllipse(full_subpage.left() + full_subpage.width()*0.1, full_subpage.bottom() - h, d - full_subpage.width()*0.1, h)
                elif h >= d:
                    top_subpage = QRect(full_subpage.left(), full_subpage.top(), d, d)
                    middle_subpage = QRect(full_subpage.left(), full_subpage.top() + r, full_subpage.width(), h - d)
                    bottom_subpage = QRect(full_subpage.left(), full_subpage.bottom() - d, d, d)
                    path.addRect(middle_subpage)
                    path.addRoundedRect(top_subpage,top_subpage.width()/2, top_subpage.width()/2)
                    path.addRoundedRect(bottom_subpage,bottom_subpage.width()/2, bottom_subpage.width()/2)

                    painter.fillPath(path,black)
                elif h < d:
                    painter.drawEllipse(full_subpage.left(),full_subpage.bottom() - h, d, h)

            return super().paintEvent(ev)
        except Exception as e: 
            print(f"pressure_slider paintEvent error: {e}")

