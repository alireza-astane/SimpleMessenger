#ifndef APICLIENT_H
#define APICLIENT_H

#include <QObject>
#include <QString>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

class ApiClient : public QObject
{
    Q_OBJECT

public:
    explicit ApiClient(QObject *parent = nullptr);
    void signup(const QString &username, const QString &password, const QString &confirmPassword, std::function<void(bool success)> callback);
    void signin(const QString &username, const QString &password, std::function<void(const QString &token)> callback);
    void fetchChats(const QString &token, std::function<void(const QJsonDocument &chats)> callback);
    void fetchChatMessages(const QString &token, const QString &chatId, std::function<void(const QJsonDocument &messages)> callback);
    void sendMessage(const QString &token, const QString &chatId, const QString &message, std::function<void(bool success)> callback);
    void clearToken();
    void createChat(const QString &token, const QString &username, std::function<void(bool success)> callback);
    QString getToken() const;
    const QMap<QString, QString>& getChatDictionary() const;
    QString getCurrentChatName();    
    QString getCurrentChatId();

private:
    QNetworkAccessManager *networkManager;
    const QString BASE_URL = "http://0.0.0.0:8000/API";
    QString token;
    QMap<QString, QString> chatDictionary; // Key: Chat name, Value: Chat ID
    QString currentChatId;
    QString currentChatName;
};

#endif // APICLIENT_H