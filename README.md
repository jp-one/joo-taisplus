# Odoo-addons-dev
VSCodeとDockerを組み合わせたOdooのカスタムモジュール用アドオン開発環境のテンプレート。  
Add-ons development environment template for Odoo's custom modules that combines VSCode and Docker.  


# はじめに Get Started

本テンプレートは、Odooのカスタムモジュール用アドオン開発環境のテンプレートです。  
This template is add-ons development environment template for Odoo's custom modules.

VSCodeとDockerを組み合わせているため、簡単にOdooのカスタムモジュール用アドオン開発環境を構築でき、すぐに開発を始めることができます。もちろん、Odoo標準のアプリケーションの動作検証を行うこともできます。  
With the combination of VSCode and Docker, you can easily build add-ons development environment for Odoo's custom modules and start developing right away. Of course, you can also verify the operation of standard Odoo applications.

次のツールをインストールしてください。  
Install the following tools.  

1. [git](https://git-scm.com/)
1. [VSCode](https://code.visualstudio.com/download)
1. [Docker](https://www.docker.com/)


# 使い方 How to use

## Using this template

1. GitHubのリポジトリを開きます。  
   Open the repository on github.  
   https://github.com/jp-rad/odoo-addons-dev

1. `Use this template`をクリックします。  
   Click `Use this template`.  
   [Here - https://github.com/jp-rad/odoo-addons-dev/generate](https://github.com/jp-rad/odoo-addons-dev/generate)


## git clone

1. コマンドプロンプトを開き、次のコマンドを実行します。  
Open the command prompt and run below commands.

```CommandPrompt.cmd
mkdir c:\workgit
cd c:\workgit
git clone <your GitHub Code URL>
```

## VSCode, Reopen in Container

1. VSCodeで、git cloneしたフォルダを開きます。  
Open the git cloned folder in VSCode.  
1. VSCodeに拡張機能「Remote - Containers」をインストールします。  
Install the "Remote - Containers" extension to VSCode.
1. VSCodeの左下に拡張機能「Remote - Containers」のアイコンが追加されますので、そのアイコンをクリックします。  
An icon for the extension "Remote - Containers" will be added to the bottom left corner of VSCode, click on that icon.  
1. 「Remote-Containers: Reopen in Container」をリストから選択します。  
Select "Remote-Containers: Reopen in Container" from the list.
1. Dockerコンテナーが起動し、VSCodeからリモート開発ができるようになります。  
The Docker container will start and you will be able to develop remotely from VSCode.


## custom_addons

1. 「custom_addons」フォルダ内で、アドオンの開発が可能です。Odooチュートリアル等を参考にしてください。  
You can develop your own add-ons in "custom_addons" folder, see the Odoo tutorials, etc.  
https://www.odoo.com/documentation/master/developer/howtos/backend.html
1. 空のモジュールを新規追加するには、次のコマンドを実行します。  
To add a new empty module, issue the following command
```
/opt/odoo/repo/odoo/odoo-bin scaffold <module name>
```

## Log in to Odoo

1. VSCodeの左にある「Debug and Run」アイコンをクリックし、「Odoo addons」を選んだ状態で、「Start Debugging」アイコンをクリックすると、Odooが起動します。  
Click on the "Debug and Run" icon on the left of VSCode, and with "Odoo addons" selected, click on the "Start Debugging" icon to start Odoo.
1. Odooが起動したら、ブラウザーを開き、Odooにアクセスして、ログインしてください（admin/admin）。  
Once Odoo is running, open your browser, access Odoo, and log in (admin/admin).  
http://localhost/


# ライセンス License

## odoo-addons-dev のライセンス

本リポジトリ「odoo-addons-dev」自体は [MITライセンス](https://opensource.org/licenses/MIT) です。  
商用・非商用問わず自由に利用・改変・再配布が可能です。  
MITライセンスの主な特徴は以下の通りです。

- ソフトウェアの利用、複製、改変、配布、サブライセンス、販売が自由
- 著作権表示とライセンス文の記載が必要
- 無保証

This repository "odoo-addons-dev" itself is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
You are free to use, modify, and redistribute it for commercial or non-commercial purposes.  
Key points of the MIT License:

- Free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
- Must include copyright notice and license text
- Provided "as is", without warranty

## 開発するOdooカスタムモジュールのライセンス

このテンプレートを利用して開発するOdooカスタムモジュール（`custom_addons`配下）は、  
[LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html) または [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html) のいずれかのライセンスを選択してください。

- **LGPLv3 (Lesser General Public License v3)**  
  Odoo本体の標準的なライセンスです。  
  商用利用やクローズドソースとの連携も可能ですが、LGPL部分の改変は公開義務があります。

- **AGPLv3 (Affero General Public License v3)**  
  OCA（Odoo Community Association）などのコミュニティモジュールで多く採用されています。  
  サーバー経由で利用する場合もソースコード公開義務が発生します。

どちらのライセンスを選択するかは、モジュールの公開方針やOdoo本体・OCAモジュールとの互換性を考慮して決定してください。

When developing your own Odoo custom modules (under `custom_addons`),  
please choose either [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html) or [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html) as the license.

- **LGPLv3**: Standard for Odoo core, allows commercial use and closed-source integration, but requires publishing modifications to LGPL parts.
- **AGPLv3**: Common for OCA modules, requires source code disclosure even for server-side use.

Choose the license according to your module's distribution policy and compatibility with Odoo/OCA modules.

## OdooおよびOCAのライセンスについて

Odoo本体やOCA（Odoo Community Association）の各モジュールのライセンスについては、  
以下のOCA公式ブログ記事を参照してください。

- [OCA / Odoo Meeting on Licenses](https://odoo-community.org/blog/news-updates-1/oca-odoo-meeting-on-licenses-21)

Odoo本体は主にLGPLv3、OCAモジュールはAGPLv3またはLGPLv3が採用されています。  
OdooやOCAモジュールを利用・改変・配布する際は、各プロジェクトのライセンス条件を必ずご確認ください。

For details on Odoo and OCA module licenses, see the following OCA official blog post:

- [OCA / Odoo Meeting on Licenses](https://odoo-community.org/blog/news-updates-1/oca-odoo-meeting-on-licenses-21)

Odoo core is mainly LGPLv3, OCA modules are AGPLv3 or LGPLv3.  
Always check the license terms of each project when using, modifying, or distributing Odoo or OCA modules.
