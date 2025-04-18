#include "mainwindow.h"
#include <QApplication>
#include <QLocale>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "MessengerClient_" + QLocale(locale).name();
    }
    MainWindow w;
    w.show();
    return a.exec();
}
