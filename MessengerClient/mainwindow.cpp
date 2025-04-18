#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QJsonArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <iostream>
#include "apiclient.h"
// #include "apiclient.h"




const QString BASE_URL = "http://0.0.0.0:8000/API";
ApiClient *apiClient = new ApiClient();

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // Connect buttons to their respective slots
    connect(ui->signInButton, &QPushButton::clicked, this, &MainWindow::onSignInClicked);
    connect(ui->signUpButton, &QPushButton::clicked, this, &MainWindow::onSignUpClicked);
    connect(ui->sendMessageButton, &QPushButton::clicked, this, &MainWindow::onSendMessageClicked);
    connect(ui->signInSubmitButton, &QPushButton::clicked, this, &MainWindow::onSignInSubmitClicked);
    connect(ui->signUpSubmitButton, &QPushButton::clicked, this, &MainWindow::onSignUpSubmitClicked);
    connect(ui->newChatButton, &QPushButton::clicked, this, &MainWindow::onNewChatClicked);
    connect(ui->signOutButton, &QPushButton::clicked, this, &MainWindow::onSignOutClicked);
    connect(ui->backButton, &QPushButton::clicked, this, &MainWindow::onBackClicked);
    connect(ui->chatsListWidget, &QListWidget::itemClicked, this, &MainWindow::onChatSelected);
    // connect(ui->chatsListWidget, &QListWidget::clicked, this, &MainWindow::onChatSelected);
    connect(ui->redirectSignInButton, &QPushButton::clicked, this, &MainWindow::onRedirectToSignInClicked);
    connect(ui->redirectSignUpButton, &QPushButton::clicked, this, &MainWindow::onRedirectToSignUpClicked);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::onRedirectToSignInClicked()
{
    ui->stackedWidget->setCurrentWidget(ui->signin_page);
}
void MainWindow::onRedirectToSignUpClicked()
{
    ui->stackedWidget->setCurrentWidget(ui->signup_page);
}
void MainWindow::onSignOutClicked()
{
    apiClient->clearToken();
    ui->stackedWidget->setCurrentWidget(ui->signin_page);
    

}

void MainWindow::onSignInClicked()
{
    ui->stackedWidget->setCurrentWidget(ui->signin_page);
}

void MainWindow::onSignUpClicked()
{
    ui->stackedWidget->setCurrentWidget(ui->signup_page);
}



void MainWindow::onBackClicked()
{
    ui->chatsListWidget->clear();
    apiClient->fetchChats(apiClient->getToken(), [this](const QJsonDocument &chats) {
        qDebug() << "Chats fetched:" << chats.toJson();

        // Populate the chats list widget with chat names
        const QMap<QString, QString> &chatDictionary = apiClient->getChatDictionary();
        for (auto it = chatDictionary.begin(); it != chatDictionary.end(); ++it) {
            QListWidgetItem *item = new QListWidgetItem(it.key()); // Chat name
            ui->chatsListWidget->addItem(item);
        }
    });

    ui->stackedWidget->setCurrentWidget(ui->chats_page);
}





void MainWindow::onSignInSubmitClicked()
{
    QString username = ui->usernameLineEdit->text();
    QString password = ui->passwordLineEdit->text();
    std::cout << "username:" << username.toStdString() << std::endl;
    std::cout << "password:" << password.toStdString() << std::endl;

    qDebug() << "Username:" << username;
    qDebug() << "Password:" << password;

    apiClient->signin(username, password, [this](const QString &token) {
        if (!token.isEmpty()) {
            qDebug() << "Token received:" << token;
            apiClient->fetchChats(token, [this](const QJsonDocument &chats) {
                qDebug() << "Chats fetched:" << chats.toJson();
                std::cout << "Chats fetched:" << chats.toJson().toStdString() << std::endl;




                // Populate the chats list widget
                const QMap<QString, QString> &chatDictionary = apiClient->getChatDictionary();
                for (auto it = chatDictionary.begin(); it != chatDictionary.end(); ++it) {

                    // print chat name and id
                    std::cout << "Chat name:" << it.key().toStdString() << ", Chat ID:" << it.value().toStdString() << std::endl;

                    QListWidgetItem *item = new QListWidgetItem(it.key()); // Chat name
                    ui->chatsListWidget->addItem(item);
                }
                // Set the current widget to the chats page
                ui->stackedWidget->setCurrentWidget(ui->chats_page);
            });
        } else {
            qDebug() << "Sign-in failed.";   //TODO Error handling for wrong username or password

        }
    });
}


void MainWindow::onSignUpSubmitClicked()
{
    // Handle sign-up logic here
    QString username = ui->usernameLineEdit->text();
    QString password = ui->passwordLineEdit->text();
    QString confirmPassword = ui->confirmPasswordLineEdit->text();

    std::cout << "username:" << username.toStdString() << std::endl;
    std::cout << "password:" << password.toStdString() << std::endl;
    std::cout << "confirmPassword:" << confirmPassword.toStdString() << std::endl;
    qDebug() << "Username:" << username;
    qDebug() << "Password:" << password;
    qDebug() << "Confirm Password:" << confirmPassword;
    apiClient->signup(username, password, confirmPassword, [this](bool success) {
        if (success) {
            qDebug() << "Sign-up successful!";
            ui->stackedWidget->setCurrentWidget(ui->signin_page);
        } else {
            qDebug() << "Sign-up failed.";   //TODO Error handling for wrong username or password
        }
    });
}



void MainWindow::onNewChatClicked()
{
    QString username = ui->newChatUsernameLineEdit->text();

    if (username.isEmpty()) {
        qDebug() << "Username is empty. Cannot create chat.";
        return;
    }

    qDebug() << "Creating chat with username:" << username;

    apiClient->createChat(apiClient->getToken(), username, [this](bool success) {
        if (success) {
            qDebug() << "Chat created successfully!";
            // Refresh the chats list
            onBackClicked();
        } else {
            qDebug() << "Failed to create chat.";
        }
    });
}


void MainWindow::onChatSelected(QListWidgetItem *item)
{
    if (!item) {
        qDebug() << "No chat selected.";
        return;
    }

    QString chatName = item->text();
    const QMap<QString, QString> &chatDictionary = apiClient->getChatDictionary();

    if (!chatDictionary.contains(chatName)) {
        qDebug() << "Chat ID not found for chat name:" << chatName;
        return;
    }

    QString chatId = chatDictionary.value(chatName);
    qDebug() << "Selected chat:" << chatName << ", Chat ID:" << chatId;

    // Fetch messages for the selected chat
    apiClient->fetchChatMessages(apiClient->getToken(), chatId, [this](const QJsonDocument &messages) {
        if (!messages.isEmpty()) {
            std::cout << "Messages fetched heeeyyyyy" <<std::endl;
            qDebug() << "Messages fetched for chat:" << messages.toJson();

            // Populate the chat messages list widget
            // set contactNameLable
            ui->contactNameLabel->setText(apiClient->getCurrentChatName()); 
            std::cout << "Contact name:" << apiClient->getCurrentChatName().toStdString() << std::endl;

            ui->chatMessagesListWidget->clear();


          





            QJsonObject rootObject = messages.object();  // Root is an object
            QJsonArray messageArray = rootObject["messages"].toArray();  // Extract the "messages" array
            std::cout << "Message array size:" << messageArray.size() << std::endl;
            for (const QJsonValue &messageValue : messageArray) {
                QJsonObject messageObject = messageValue.toObject();
                QString content = messageObject["text"].toString(); //TODO Show the sender 
                QString message = content;
                ui->chatMessagesListWidget->addItem(message);
            }

            // Switch to the chat page
            ui->stackedWidget->setCurrentWidget(ui->chat_page);
        } else {
            qDebug() << "Failed to fetch messages for chat.";
        }
    });
}

void MainWindow::onSendMessageClicked()
{
    QString message = ui->messageInputLineEdit->text();
    if (message.isEmpty()) {
        qDebug() << "Message is empty. Cannot send.";
        return;
    }

    // Get the current chat ID from the chat dictionary
    QString currentChatId = apiClient->getCurrentChatId();

    if (currentChatId.isEmpty()) {
        qDebug() << "No chat selected. Cannot send message.";
        return;
    }

    qDebug() << "Sending message to chat ID:" << currentChatId << ", Message:" << message;

    // Call the ApiClient to send the message
    std::cout << "Sending message:" << message.toStdString() << std::endl;
    apiClient->sendMessage(apiClient->getToken(), currentChatId, message, [this, message](bool success) { // Fixed: Capture `message`
        if (success) {
            qDebug() << "Message sent successfully!";
            ui->chatMessagesListWidget->addItem("You: " + message); // Add the message to the UI
            ui->messageInputLineEdit->clear();
        } else {
            qDebug() << "Failed to send message.";
        }
    });
}
