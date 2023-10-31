# Online_Chat_Messenger

## 概要
クライアントサーバ型のアプリケーションの一つで、オンラインでメッセージを送れるチャットメッセンジャーです。

クライアントがチャットルームを作成し、参加できるサービスを構築します。各チャットルームは独自のキーで特定され、そのキーは他のユーザーが参加できるようにします。新しいチャットルームを作成するには、タイトルと最大参加者数を指定します。このサービスはデータの損失を防ぐためにTCP接続を使用します。チャットルーム作成時、クライアントは自動的にUDPでチャットルームに接続し、ホストになります。各チャットルームはハッシュマップとして実装され、チャットルーム情報を含むオブジェクトです。ChatClientはクライアントの情報を保持するオブジェクトで、アドレスとポートを組み合わせてユニークに識別します。各クライアントは1つのチャットルームにのみ参加可能で、最大参加者数を超えることはできません。メッセージの送信には特定のプレフィックスが必要で、送信者の参加を確認する必要があります。チャットルームに参加するには特定のメッセージをサーバに送信します。

## 作成の経緯
オペレーティングシステムのソケット API を使用してアプリケーションがどのようにデータを送信するかを学習するために作成しました。

## 使用技術
Python

## 環境
OS : Ubuntu

エディタ：Visual Studio Code

## 作成期間
2023/10/20~2023/10/27

## 使用方法
1　ユーザーはルーム作成、ルームに加入、メッセージを送る、の3つのコマンドの中で行いたい動作を選びます。

# ルーム作成、を選んだ場合 
2　ルーム作成を選んだ場合、ルーム名と部屋の最大人数を入力します。

3　ルームが作成されます。

# ルームに加入、を選んだ場合
2　ルームに加入を選んだ場合、どのルームに入るのか聞かれます。ルーム名を入力して、実際に存在するルームであれば、加入できます。実在しなければエラーが出ます。

3　サーバ側でルームメンバーは確認できます。

# メッセージを送る、を選んだ場合
2　ユーザーがそのルームのメンバーであるとき、メッセージを他のルームメイトに送れます。送りたいメッセージを入力してください。



