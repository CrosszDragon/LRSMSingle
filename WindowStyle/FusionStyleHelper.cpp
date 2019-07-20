/*
 * Below there are a lot of helper functions which are copied from various
 * private Qt parts that are used by the Fusion style, on which the Tiled style
 * is based.
 *
 * These parts are Copyright (C) 2015 The Qt Company Ltd.
 * Used under the terms of the GNU Lesser General Public License version 2.1
 */

// internal helper. Converts an integer value to an unique string token
template <typename T>
        struct HexString
{
    inline explicit HexString(const T t)
        : val(t)
    {}
    inline void write(QChar *&dest) const
    {
        const ushort hexChars[] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
        const char *c = reinterpret_cast<const char *>(&val);
        for (uint i = 0; i < sizeof(T); ++i) {
            *dest++ = hexChars[*c & 0xf];
            *dest++ = hexChars[(*c & 0xf0) >> 4];
            ++c;
        }
    }
    const T val;
};
// specialization to enable fast concatenating of our string tokens to a string
template <typename T>
        struct QConcatenable<HexString<T> >
{
    typedef HexString<T> type;
    enum { ExactSize = true };
    static int size(const HexString<T> &) { return sizeof(T) * 2; }
    static inline void appendTo(const HexString<T> &str, QChar *&out) { str.write(out); }
    typedef QString ConvertTo;
};

static QString uniqueName(const QString &key, const QStyleOption *option, QSize size)
{
    const QStyleOptionComplex *complexOption = qstyleoption_cast<const QStyleOptionComplex *>(option);
    QString tmp = key % HexString<uint>(option->state)
                      % HexString<uint>(option->direction)
                      % HexString<uint>(complexOption ? uint(complexOption->activeSubControls) : 0u)
                      % HexString<quint64>(option->palette.cacheKey())
                      % HexString<uint>(size.width())
                      % HexString<uint>(size.height());

    if (const QStyleOptionSpinBox *spinBox = qstyleoption_cast<const QStyleOptionSpinBox *>(option)) {
        tmp = tmp % HexString<uint>(spinBox->buttonSymbols)
                  % HexString<uint>(spinBox->stepEnabled)
                  % QLatin1Char(spinBox->frame ? '1' : '0'); ;
    }

    return tmp;
}

static QColor mergedColors(const QColor &colorA, const QColor &colorB, int factor = 50)
{
    const int maxFactor = 100;
    QColor tmp = colorA;
    tmp.setRed((tmp.red() * factor) / maxFactor + (colorB.red() * (maxFactor - factor)) / maxFactor);
    tmp.setGreen((tmp.green() * factor) / maxFactor + (colorB.green() * (maxFactor - factor)) / maxFactor);
    tmp.setBlue((tmp.blue() * factor) / maxFactor + (colorB.blue() * (maxFactor - factor)) / maxFactor);
    return tmp;
}

static inline QPixmap styleCachePixmap(const QSize &size)
{
    const qreal pixelRatio = qApp->devicePixelRatio();
    QPixmap cachePixmap = QPixmap(size * pixelRatio);
    cachePixmap.setDevicePixelRatio(pixelRatio);
    return cachePixmap;
}

static void qt_fusion_draw_arrow(Qt::ArrowType type, QPainter *painter, const QStyleOption *option, const QRect &rect, const QColor &color)
{
    const int arrowWidth = Utils::dpiScaled(14);
    const int arrowHeight = Utils::dpiScaled(8);

    const int arrowMax = qMin(arrowHeight, arrowWidth);
    const int rectMax = qMin(rect.height(), rect.width());
    const int size = qMin(arrowMax, rectMax);

    QPixmap cachePixmap;
    QString cacheKey = uniqueName(QLatin1String("fusion-arrow"), option, rect.size())
            % HexString<uint>(type)
            % HexString<uint>(color.rgba());
    if (!QPixmapCache::find(cacheKey, cachePixmap)) {
        cachePixmap = styleCachePixmap(rect.size());
        cachePixmap.fill(Qt::transparent);
        QPainter cachePainter(&cachePixmap);

        QRectF arrowRect;
        arrowRect.setWidth(size);
        arrowRect.setHeight(arrowHeight * size / arrowWidth);
        if (type == Qt::LeftArrow || type == Qt::RightArrow)
            arrowRect = QRectF(arrowRect.topLeft(), arrowRect.size().transposed());
        arrowRect.moveTo((rect.width() - arrowRect.width()) / 2.0,
                         (rect.height() - arrowRect.height()) / 2.0);

        QPolygonF triangle;
        triangle.reserve(3);
        switch (type) {
        case Qt::DownArrow:
            triangle << arrowRect.topLeft() << arrowRect.topRight() << QPointF(arrowRect.center().x(), arrowRect.bottom());
            break;
        case Qt::RightArrow:
            triangle << arrowRect.topLeft() << arrowRect.bottomLeft() << QPointF(arrowRect.right(), arrowRect.center().y());
            break;
        case Qt::LeftArrow:
            triangle << arrowRect.topRight() << arrowRect.bottomRight() << QPointF(arrowRect.left(), arrowRect.center().y());
            break;
        default:
            triangle << arrowRect.bottomLeft() << arrowRect.bottomRight() << QPointF(arrowRect.center().x(), arrowRect.top());
            break;
        }

        cachePainter.setPen(Qt::NoPen);
        cachePainter.setBrush(color);
        cachePainter.setRenderHint(QPainter::Antialiasing);
        cachePainter.drawPolygon(triangle);

        QPixmapCache::insert(cacheKey, cachePixmap);
    }

    painter->drawPixmap(rect, cachePixmap);
}

enum Direction {
    TopDown,
    FromLeft,
    BottomUp,
    FromRight
};

// The default button and handle gradient
static QLinearGradient qt_fusion_gradient(const QRect &rect, const QBrush &baseColor, Direction direction = TopDown)
{
    int x = rect.center().x();
    int y = rect.center().y();
    QLinearGradient gradient;
    switch (direction) {
    case FromLeft:
        gradient = QLinearGradient(rect.left(), y, rect.right(), y);
        break;
    case FromRight:
        gradient = QLinearGradient(rect.right(), y, rect.left(), y);
        break;
    case BottomUp:
        gradient = QLinearGradient(x, rect.bottom(), x, rect.top());
        break;
    case TopDown:
    default:
        gradient = QLinearGradient(x, rect.top(), x, rect.bottom());
        break;
    }
    if (baseColor.gradient())
        gradient.setStops(baseColor.gradient()->stops());
    else {
        QColor gradientStartColor = baseColor.color().lighter(124);
        QColor gradientStopColor = baseColor.color().lighter(102);
        gradient.setColorAt(0, gradientStartColor);
        gradient.setColorAt(1, gradientStopColor);
    }
    return gradient;
}

static QColor getOutlineColor(const QPalette &pal)
{
    return pal.window().color().darker(140);
}

static QColor getLightOutlineColor(const QPalette &pal)
{
    return pal.window().color().lighter(140);
}

static QColor getHighlightedOutline(const QPalette &pal)
{
    QColor highlightedOutline = pal.highlight().color().darker(125);
    if (highlightedOutline.value() > 160)
        highlightedOutline.setHsl(highlightedOutline.hue(), highlightedOutline.saturation(), 160);
    return highlightedOutline;
}

static QColor getSliderColor(const QPalette &pal, bool isDarkBg)
{
    return isDarkBg ? pal.button().color() : pal.window().color().darker(170);
}

static QColor getSliderOutline(const QPalette &pal, bool isDarkBg)
{
    return isDarkBg ? getOutlineColor(pal) : getSliderColor(pal, isDarkBg);
}

static QColor getButtonColor(const QPalette &pal)
{
    QColor buttonColor = pal.button().color();
    int val = qGray(buttonColor.rgb());
    buttonColor = buttonColor.lighter(100 + qMax(1, (180 - val)/6));
    buttonColor.setHsv(buttonColor.hue(), buttonColor.saturation() * 0.75, buttonColor.value());
    return buttonColor;
}

static QColor innerContrastLine()
{
    return QColor(255, 255, 255, 30);
}

static QColor lightShade()
{
    return QColor(255, 255, 255, 90);
}

static QColor darkShade()
{
    return QColor(0, 0, 0, 60);
}

static QColor getTabFrameColor(const QPalette &pal)
{
    return getButtonColor(pal).lighter(104);
}

static qreal roundedRectRadius()
{
    static qreal radius = Utils::dpiScaled(2.0);
    return radius;
}
