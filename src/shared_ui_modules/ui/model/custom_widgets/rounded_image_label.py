from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPainterPath, QPixmap
from PySide6.QtCore import Qt, QRectF

class RoundedImageLabel(QLabel):
    def __init__(self, antialiasing=True):
        super().__init__()
        
        self.Antialiasing = antialiasing
        self.setMinimumHeight(0)
        self.setMinimumWidth(0)
        
        self.radius = self.width() // 2
        
    def setPixmap(self, pixmap: QPixmap):
        self._raw_pixmap = pixmap

        scaled = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        target = QPixmap(self.size())
        target.fill(Qt.transparent)

        painter = QPainter(target)
        if self.Antialiasing:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), self.radius, self.radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()
        super().setPixmap(target)