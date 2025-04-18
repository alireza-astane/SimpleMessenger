/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.9.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
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
    QLabel *label_8;
    QPushButton *redirectSignUpButton;
    QWidget *signup_page;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLineEdit *signUpUsernameLineEdit;
    QLineEdit *signUpPasswordLineEdit;
    QLineEdit *confirmPasswordLineEdit;
    QPushButton *signUpSubmitButton;
    QPushButton *redirectSignInButton;
    QLabel *label_9;
    QWidget *chats_page;
    QPushButton *newChatButton;
    QPushButton *signOutButton;
    QLineEdit *newChatUsernameLineEdit;
    QListWidget *chatsListWidget;
    QLabel *label_7;
    QWidget *chat_page;
    QListWidget *chatMessagesListWidget;
    QLineEdit *messageInputLineEdit;
    QPushButton *sendMessageButton;
    QPushButton *backButton;
    QLabel *contactNameLabel;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        stackedWidget = new QStackedWidget(centralwidget);
        stackedWidget->setObjectName(QStringLiteral("stackedWidget"));
        stackedWidget->setGeometry(QRect(10, 0, 801, 571));
        welcome_page = new QWidget();
        welcome_page->setObjectName(QStringLiteral("welcome_page"));
        label = new QLabel(welcome_page);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(310, 228, 171, 20));
        signUpButton = new QPushButton(welcome_page);
        signUpButton->setObjectName(QStringLiteral("signUpButton"));
        signUpButton->setGeometry(QRect(300, 290, 80, 26));
        signInButton = new QPushButton(welcome_page);
        signInButton->setObjectName(QStringLiteral("signInButton"));
        signInButton->setGeometry(QRect(400, 290, 80, 26));
        stackedWidget->addWidget(welcome_page);
        signin_page = new QWidget();
        signin_page->setObjectName(QStringLiteral("signin_page"));
        signInSubmitButton = new QPushButton(signin_page);
        signInSubmitButton->setObjectName(QStringLiteral("signInSubmitButton"));
        signInSubmitButton->setGeometry(QRect(360, 330, 80, 26));
        passwordLineEdit = new QLineEdit(signin_page);
        passwordLineEdit->setObjectName(QStringLiteral("passwordLineEdit"));
        passwordLineEdit->setGeometry(QRect(380, 290, 151, 26));
        passwordLineEdit->setEchoMode(QLineEdit::Password);
        usernameLineEdit = new QLineEdit(signin_page);
        usernameLineEdit->setObjectName(QStringLiteral("usernameLineEdit"));
        usernameLineEdit->setGeometry(QRect(380, 250, 151, 26));
        label_2 = new QLabel(signin_page);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(280, 250, 71, 18));
        label_3 = new QLabel(signin_page);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(280, 290, 58, 18));
        label_8 = new QLabel(signin_page);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(280, 360, 161, 18));
        redirectSignUpButton = new QPushButton(signin_page);
        redirectSignUpButton->setObjectName(QStringLiteral("redirectSignUpButton"));
        redirectSignUpButton->setGeometry(QRect(440, 360, 80, 26));
        stackedWidget->addWidget(signin_page);
        signup_page = new QWidget();
        signup_page->setObjectName(QStringLiteral("signup_page"));
        label_4 = new QLabel(signup_page);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(280, 230, 71, 18));
        label_5 = new QLabel(signup_page);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(280, 260, 58, 18));
        label_6 = new QLabel(signup_page);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(257, 290, 111, 20));
        signUpUsernameLineEdit = new QLineEdit(signup_page);
        signUpUsernameLineEdit->setObjectName(QStringLiteral("signUpUsernameLineEdit"));
        signUpUsernameLineEdit->setGeometry(QRect(400, 230, 113, 26));
        signUpPasswordLineEdit = new QLineEdit(signup_page);
        signUpPasswordLineEdit->setObjectName(QStringLiteral("signUpPasswordLineEdit"));
        signUpPasswordLineEdit->setGeometry(QRect(400, 260, 113, 26));
        signUpPasswordLineEdit->setEchoMode(QLineEdit::Password);
        confirmPasswordLineEdit = new QLineEdit(signup_page);
        confirmPasswordLineEdit->setObjectName(QStringLiteral("confirmPasswordLineEdit"));
        confirmPasswordLineEdit->setGeometry(QRect(400, 290, 113, 26));
        confirmPasswordLineEdit->setEchoMode(QLineEdit::Password);
        signUpSubmitButton = new QPushButton(signup_page);
        signUpSubmitButton->setObjectName(QStringLiteral("signUpSubmitButton"));
        signUpSubmitButton->setGeometry(QRect(370, 330, 80, 26));
        redirectSignInButton = new QPushButton(signup_page);
        redirectSignInButton->setObjectName(QStringLiteral("redirectSignInButton"));
        redirectSignInButton->setGeometry(QRect(430, 370, 80, 26));
        label_9 = new QLabel(signup_page);
        label_9->setObjectName(QStringLiteral("label_9"));
        label_9->setGeometry(QRect(260, 370, 161, 18));
        stackedWidget->addWidget(signup_page);
        chats_page = new QWidget();
        chats_page->setObjectName(QStringLiteral("chats_page"));
        newChatButton = new QPushButton(chats_page);
        newChatButton->setObjectName(QStringLiteral("newChatButton"));
        newChatButton->setGeometry(QRect(0, 530, 80, 26));
        signOutButton = new QPushButton(chats_page);
        signOutButton->setObjectName(QStringLiteral("signOutButton"));
        signOutButton->setGeometry(QRect(720, 530, 80, 26));
        newChatUsernameLineEdit = new QLineEdit(chats_page);
        newChatUsernameLineEdit->setObjectName(QStringLiteral("newChatUsernameLineEdit"));
        newChatUsernameLineEdit->setGeometry(QRect(90, 530, 113, 26));
        chatsListWidget = new QListWidget(chats_page);
        chatsListWidget->setObjectName(QStringLiteral("chatsListWidget"));
        chatsListWidget->setGeometry(QRect(80, 80, 641, 241));
        label_7 = new QLabel(chats_page);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(370, 40, 58, 18));
        stackedWidget->addWidget(chats_page);
        chat_page = new QWidget();
        chat_page->setObjectName(QStringLiteral("chat_page"));
        chatMessagesListWidget = new QListWidget(chat_page);
        chatMessagesListWidget->setObjectName(QStringLiteral("chatMessagesListWidget"));
        chatMessagesListWidget->setGeometry(QRect(70, 90, 661, 361));
        messageInputLineEdit = new QLineEdit(chat_page);
        messageInputLineEdit->setObjectName(QStringLiteral("messageInputLineEdit"));
        messageInputLineEdit->setGeometry(QRect(162, 470, 571, 26));
        sendMessageButton = new QPushButton(chat_page);
        sendMessageButton->setObjectName(QStringLiteral("sendMessageButton"));
        sendMessageButton->setGeometry(QRect(70, 470, 80, 26));
        backButton = new QPushButton(chat_page);
        backButton->setObjectName(QStringLiteral("backButton"));
        backButton->setGeometry(QRect(0, 30, 80, 26));
        backButton->setFlat(false);
        contactNameLabel = new QLabel(chat_page);
        contactNameLabel->setObjectName(QStringLiteral("contactNameLabel"));
        contactNameLabel->setGeometry(QRect(350, 50, 111, 18));
        stackedWidget->addWidget(chat_page);
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 23));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        backButton->setDefault(false);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", Q_NULLPTR));
        label->setText(QApplication::translate("MainWindow", "Welcome to the messenger ", Q_NULLPTR));
        signUpButton->setText(QApplication::translate("MainWindow", "Sign up", Q_NULLPTR));
        signInButton->setText(QApplication::translate("MainWindow", "Sign in", Q_NULLPTR));
        signInSubmitButton->setText(QApplication::translate("MainWindow", "Sign in", Q_NULLPTR));
        passwordLineEdit->setText(QString());
        usernameLineEdit->setText(QString());
        label_2->setText(QApplication::translate("MainWindow", "Username ", Q_NULLPTR));
        label_3->setText(QApplication::translate("MainWindow", "Password", Q_NULLPTR));
        label_8->setText(QApplication::translate("MainWindow", "Don't have an account?", Q_NULLPTR));
        redirectSignUpButton->setText(QApplication::translate("MainWindow", "Sign Up", Q_NULLPTR));
        label_4->setText(QApplication::translate("MainWindow", "Username", Q_NULLPTR));
        label_5->setText(QApplication::translate("MainWindow", "Password", Q_NULLPTR));
        label_6->setText(QApplication::translate("MainWindow", "Confirm Password", Q_NULLPTR));
        signUpSubmitButton->setText(QApplication::translate("MainWindow", "Sign Up", Q_NULLPTR));
        redirectSignInButton->setText(QApplication::translate("MainWindow", "Sign In", Q_NULLPTR));
        label_9->setText(QApplication::translate("MainWindow", "Already have an account? ", Q_NULLPTR));
        newChatButton->setText(QApplication::translate("MainWindow", "New Chat", Q_NULLPTR));
        signOutButton->setText(QApplication::translate("MainWindow", "Sign out", Q_NULLPTR));
        label_7->setText(QApplication::translate("MainWindow", "Chats:", Q_NULLPTR));
        sendMessageButton->setText(QApplication::translate("MainWindow", "Send", Q_NULLPTR));
        backButton->setText(QApplication::translate("MainWindow", "Back", Q_NULLPTR));
        contactNameLabel->setText(QApplication::translate("MainWindow", "Contact Name ", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
