/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MESSENGER_H
#define UI_MESSENGER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QStackedWidget *stackedWidget;
    QWidget *welcome_page;
    QLabel *label;
    QPushButton *signUpButton;
    QPushButton *signInButton;
    QWidget *signin_page;
    QPushButton *signInSubmitButton;
    QLineEdit *passwordLineEdit;
    QLineEdit *usernameLineEdit;
    QLabel *label_2;
    QLabel *label_3;
    QWidget *signup_page;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLineEdit *signUpUsernameLineEdit;
    QLineEdit *signUpPasswordLineEdit;
    QLineEdit *confirmPasswordLineEdit;
    QPushButton *signUpSubmitButton;
    QWidget *chats_page;
    QPushButton *newChatButton;
    QPushButton *signOutButton;
    QLineEdit *newChatUsernameLineEdit;
    QListWidget *chatsListWidget;
    QWidget *chat_page;
    QListWidget *chatMessagesListWidget;
    QLineEdit *messageInputLineEdit;
    QPushButton *sendMessageButton;
    QPushButton *backButton;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        stackedWidget = new QStackedWidget(centralwidget);
        stackedWidget->setObjectName(QString::fromUtf8("stackedWidget"));
        stackedWidget->setGeometry(QRect(10, 0, 801, 571));
        welcome_page = new QWidget();
        welcome_page->setObjectName(QString::fromUtf8("welcome_page"));
        label = new QLabel(welcome_page);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(310, 228, 171, 20));
        signUpButton = new QPushButton(welcome_page);
        signUpButton->setObjectName(QString::fromUtf8("signUpButton"));
        signUpButton->setGeometry(QRect(300, 290, 80, 26));
        signInButton = new QPushButton(welcome_page);
        signInButton->setObjectName(QString::fromUtf8("signInButton"));
        signInButton->setGeometry(QRect(400, 290, 80, 26));
        stackedWidget->addWidget(welcome_page);
        signin_page = new QWidget();
        signin_page->setObjectName(QString::fromUtf8("signin_page"));
        signInSubmitButton = new QPushButton(signin_page);
        signInSubmitButton->setObjectName(QString::fromUtf8("signInSubmitButton"));
        signInSubmitButton->setGeometry(QRect(360, 330, 80, 26));
        passwordLineEdit = new QLineEdit(signin_page);
        passwordLineEdit->setObjectName(QString::fromUtf8("passwordLineEdit"));
        passwordLineEdit->setGeometry(QRect(380, 290, 151, 26));
        passwordLineEdit->setEchoMode(QLineEdit::Password);
        usernameLineEdit = new QLineEdit(signin_page);
        usernameLineEdit->setObjectName(QString::fromUtf8("usernameLineEdit"));
        usernameLineEdit->setGeometry(QRect(380, 250, 151, 26));
        label_2 = new QLabel(signin_page);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(280, 250, 71, 18));
        label_3 = new QLabel(signin_page);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(280, 290, 58, 18));
        stackedWidget->addWidget(signin_page);
        signup_page = new QWidget();
        signup_page->setObjectName(QString::fromUtf8("signup_page"));
        label_4 = new QLabel(signup_page);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(280, 230, 71, 18));
        label_5 = new QLabel(signup_page);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(280, 260, 58, 18));
        label_6 = new QLabel(signup_page);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(257, 290, 111, 20));
        signUpUsernameLineEdit = new QLineEdit(signup_page);
        signUpUsernameLineEdit->setObjectName(QString::fromUtf8("signUpUsernameLineEdit"));
        signUpUsernameLineEdit->setGeometry(QRect(400, 230, 113, 26));
        signUpPasswordLineEdit = new QLineEdit(signup_page);
        signUpPasswordLineEdit->setObjectName(QString::fromUtf8("signUpPasswordLineEdit"));
        signUpPasswordLineEdit->setGeometry(QRect(400, 260, 113, 26));
        signUpPasswordLineEdit->setEchoMode(QLineEdit::Password);
        confirmPasswordLineEdit = new QLineEdit(signup_page);
        confirmPasswordLineEdit->setObjectName(QString::fromUtf8("confirmPasswordLineEdit"));
        confirmPasswordLineEdit->setGeometry(QRect(400, 290, 113, 26));
        confirmPasswordLineEdit->setEchoMode(QLineEdit::Password);
        signUpSubmitButton = new QPushButton(signup_page);
        signUpSubmitButton->setObjectName(QString::fromUtf8("signUpSubmitButton"));
        signUpSubmitButton->setGeometry(QRect(370, 330, 80, 26));
        stackedWidget->addWidget(signup_page);
        chats_page = new QWidget();
        chats_page->setObjectName(QString::fromUtf8("chats_page"));
        newChatButton = new QPushButton(chats_page);
        newChatButton->setObjectName(QString::fromUtf8("newChatButton"));
        newChatButton->setGeometry(QRect(0, 530, 80, 26));
        pushButton_2 = new QPushButton(chats_page);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setGeometry(QRect(720, 530, 80, 26));
        newChatUsernameLineEdit = new QLineEdit(chats_page);
        newChatUsernameLineEdit->setObjectName(QString::fromUtf8("newChatUsernameLineEdit"));
        newChatUsernameLineEdit->setGeometry(QRect(90, 530, 113, 26));
        chatsListWidget = new QListWidget(chats_page);
        chatsListWidget->setObjectName(QString::fromUtf8("chatsListWidget"));
        chatsListWidget->setGeometry(QRect(80, 80, 641, 241));
        stackedWidget->addWidget(chats_page);
        chat_page = new QWidget();
        chat_page->setObjectName(QString::fromUtf8("chat_page"));
        chatMessagesListWidget = new QListWidget(chat_page);
        chatMessagesListWidget->setObjectName(QString::fromUtf8("chatMessagesListWidget"));
        chatMessagesListWidget->setGeometry(QRect(70, 90, 661, 361));
        messageInputLineEdit = new QLineEdit(chat_page);
        messageInputLineEdit->setObjectName(QString::fromUtf8("messageInputLineEdit"));
        messageInputLineEdit->setGeometry(QRect(162, 470, 571, 26));
        sendMessageButton = new QPushButton(chat_page);
        sendMessageButton->setObjectName(QString::fromUtf8("sendMessageButton"));
        sendMessageButton->setGeometry(QRect(70, 470, 80, 26));
        backButton = new QPushButton(chat_page);
        backButton->setObjectName(QString::fromUtf8("backButton"));
        backButton->setGeometry(QRect(0, 30, 80, 26));
        backButton->setFlat(false);
        stackedWidget->addWidget(chat_page);
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 23));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        backButton->setDefault(false);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Welcome to the messenger ", nullptr));
        signUpButton->setText(QCoreApplication::translate("MainWindow", "Sign up", nullptr));
        signInButton->setText(QCoreApplication::translate("MainWindow", "Sign in", nullptr));
        signInSubmitButton->setText(QCoreApplication::translate("MainWindow", "Sign in", nullptr));
        passwordLineEdit->setText(QString());
        usernameLineEdit->setText(QString());
        label_2->setText(QCoreApplication::translate("MainWindow", "Username ", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "Password", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "Username", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "Password", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "Confirm Password", nullptr));
        signUpSubmitButton->setText(QCoreApplication::translate("MainWindow", "Sign Up", nullptr));
        newChatButton->setText(QCoreApplication::translate("MainWindow", "New Chat", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "Sign out", nullptr));
        sendMessageButton->setText(QCoreApplication::translate("MainWindow", "Send", nullptr));
        backButton->setText(QCoreApplication::translate("MainWindow", "Back", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MESSENGER_H
