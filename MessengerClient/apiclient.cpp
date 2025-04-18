#include "apiclient.h"
#include <QUrl>
#include <QNetworkRequest>
#include <QByteArray>
#include <QDebug>
#include <iostream>
#include <QJsonArray>
#include <QJsonDocument>




ApiClient::ApiClient(QObject *parent)
    : QObject(parent), networkManager(new QNetworkAccessManager(this))
{
}
void ApiClient::signup(const QString &username, const QString &password, const QString &confirmPassword, std::function<void(bool success)> callback)
{
    // Check if the password and confirm password match
    if (password != confirmPassword) {
        qDebug() << "Passwords do not match!";
        return;
    }

    // Proceed with the signup process
    QUrl url(BASE_URL + "/signup");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

    QByteArray data;
    data.append("username=" + username.toUtf8() + "&");
    data.append("password=" + password.toUtf8() + "&");
    data.append("confirm_password=" + confirmPassword.toUtf8());

    QNetworkReply *reply = networkManager->post(request, data);

    connect(reply, &QNetworkReply::finished, [reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            qDebug() << "Signup successful:" << reply->readAll();
        } else {
            qDebug() << "Signup failed:" << reply->errorString();
        }
        reply->deleteLater();
    });
}

void ApiClient::signin(const QString &username, const QString &password, std::function<void(const QString &token)> callback)
{
    QUrl url(BASE_URL + "/signin");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");

    QByteArray data;
    data.append("username=" + username.toUtf8() + "&");
    data.append("password=" + password.toUtf8());

    QNetworkReply *reply = networkManager->post(request, data);

    connect(reply, &QNetworkReply::finished, [this, reply, callback]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument jsonResponse = QJsonDocument::fromJson(reply->readAll());
            QString token = jsonResponse.object().value("access_token").toString();
            qDebug() << "Login successful! Token:" << token;
            std::cout << "Login successful! Token:" << token.toStdString() << std::endl;
            callback(token);
            this->token = token;  // Store the token for later use
        } else {
            qDebug() << "Login failed:" << reply->errorString();
            std::cout << "Login failed:" << reply->errorString().toStdString() << std::endl;
            callback("");
        }
        reply->deleteLater();
    });
}

void ApiClient::fetchChats(const QString &token, std::function<void(const QJsonDocument &chats)> callback)
{
    QUrl url(BASE_URL + "/chats");
    QNetworkRequest request(url);
    request.setRawHeader("Authorization", "Bearer " + token.toUtf8());

    QNetworkReply *reply = networkManager->get(request);

    connect(reply, &QNetworkReply::finished, [this, reply, callback]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument jsonResponse = QJsonDocument::fromJson(reply->readAll());
            qDebug() << "Chats fetched:" << jsonResponse.toJson();
            std::cout << "Chats fetched successfully" << std::endl;

            // Parse the JSON response
            QJsonObject rootObject = jsonResponse.object();  // Root is an object
            QJsonArray chatArray = rootObject["chats"].toArray();  // Extract the "chats" array
            std::cout << "Chat array size:" << chatArray.size() << std::endl;

            // Clear the dictionary and populate it with the new data
            this->chatDictionary.clear();
            for (const QJsonValue &chatValue : chatArray) {
                QJsonObject chatObject = chatValue.toObject();
                QString chatName = chatObject["name"].toString();
                QString chatId = chatObject["id"].toString();
                std::cout << "Chat name:" << chatName.toStdString() << ", Chat ID:" << chatId.toStdString() << std::endl;
                this->chatDictionary.insert(chatName, chatId);
            }

            callback(jsonResponse);
        } else {
            qDebug() << "Failed to fetch chats:" << reply->errorString();
            std::cout << "Failed to fetch chats:" << reply->errorString().toStdString() << std::endl;
            callback(QJsonDocument());
        }
        reply->deleteLater();
    });
}


void ApiClient::fetchChatMessages(const QString &token, const QString &chatId, std::function<void(const QJsonDocument &messages)> callback)
{
    QUrl url(BASE_URL + "/chat/" + chatId);
    QNetworkRequest request(url);
    request.setRawHeader("Authorization", "Bearer " + token.toUtf8());

    QNetworkReply *reply = networkManager->get(request);

    // Capture `this` in the lambda to access non-static members
    connect(reply, &QNetworkReply::finished, [this, reply, callback, chatId]() {
        if (reply->error() == QNetworkReply::NoError) {
            QJsonDocument jsonResponse = QJsonDocument::fromJson(reply->readAll());
            qDebug() << "Messages for chat:" << jsonResponse.toJson();
            std::cout << "Messages for chat:" << jsonResponse.toJson().toStdString() << std::endl;

            // Set current chat ID and name from the dictionary 
            QString chatName = this->chatDictionary.key(chatId);
            this->currentChatId = chatId;
            this->currentChatName = chatName;
            qDebug() << "Current chat ID:" << this->currentChatId;
            qDebug() << "Current chat name:" << this->currentChatName;

            callback(jsonResponse);
        } else {
            qDebug() << "Failed to fetch messages:" << reply->errorString();
            callback(QJsonDocument());
        }
        reply->deleteLater();
    });
}

void ApiClient::sendMessage(const QString &token, const QString &chatId, const QString &message, std::function<void(bool success)> callback)
{
    QUrl url(BASE_URL + "/chat/" + chatId + "/message");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");
    request.setRawHeader("Authorization", "Bearer " + token.toUtf8());

    QByteArray data;
    data.append("message=" + message.toUtf8());

    QNetworkReply *reply = networkManager->post(request, data);
    std::cout << "Sending message:" << message.toStdString() << std::endl;

    connect(reply, &QNetworkReply::finished, [reply, callback]() {
        if (reply->error() == QNetworkReply::NoError) {
            qDebug() << "Message sent successfully!";
            std::cout << "Message sent successfully!" << std::endl;
            callback(true);
        } else {
            qDebug() << "Failed to send message:" << reply->errorString();
            std::cout << "Failed to send message:" << reply->errorString().toStdString() << std::endl;
            callback(false);
        }
        reply->deleteLater();
    });
}

void ApiClient::clearToken()
{
    token.clear();
    qDebug() << "Tokens cleared";
}

QString ApiClient::getToken() const
{
    return token;
}

const QMap<QString, QString>& ApiClient::getChatDictionary() const
{
    return chatDictionary;
}



void ApiClient::createChat(const QString &token, const QString &username, std::function<void(bool success)> callback)
{
    QUrl url(BASE_URL + "/chats/create");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/x-www-form-urlencoded");
    request.setRawHeader("Authorization", "Bearer " + token.toUtf8());

    QByteArray data;
    data.append("recipient_username=" + username.toUtf8());

    QNetworkReply *reply = networkManager->post(request, data);

    connect(reply, &QNetworkReply::finished, [reply, callback]() {
        if (reply->error() == QNetworkReply::NoError) {
            qDebug() << "Chat created successfully!";
            callback(true);
        } else {
            qDebug() << "Failed to create chat:" << reply->errorString();
            callback(false);
        }
        reply->deleteLater();
    });
}



QString ApiClient::getCurrentChatName()
{
    return currentChatName;
}

QString ApiClient::getCurrentChatId()
{
    return currentChatId;
}





