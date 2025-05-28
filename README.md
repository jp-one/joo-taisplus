# TAIS+ モジュール (TAISプラス)

`TAIS+`モジュール (`tais_plus`) は、Odooプラットフォームの機能を拡張し強化するためのカスタムモジュールです。特定のビジネスニーズに合わせた追加機能を提供します。
**特に、福祉用具の製造、販売、貸与、または管理を行う事業者向けに最適化されています。**  

## 特徴

- Odooのワークフローをカスタマイズして強化
- TAISコードおよび分類コードに基づく福祉用具管理機能
- 貸与価格の上限管理機能
- 福祉用具の全国平均貸与価格および貸与価格の上限一覧をインポート可能
- 他のOdooモジュールとの統合
- **EXCEL VBAからのAPI利用が可能**であり、貸与価格の上限を取得可能

## 背景

`TAIS+`モジュール (`tais_plus`) は、福祉用具情報システム（TAIS, タイス）に基づく管理と検索機能をサポートするために設計されています。
TAISコードは、5桁の「企業コード」と6桁の「福祉用具コード」を組み合わせた管理コードであり、福祉用具の情報共有と効率的な検索を可能にします。
また、福祉用具の全国平均貸与価格及び貸与価格の上限一覧を元に、適切な価格での貸与を可能にします。

### TAISコードとは

TAISコードは、以下の形式で構成されています：
- **例:** `00001-000010`

このコードを使用することで、登録された福祉用具を簡単に検索・閲覧することができます。1つの製品には1つのTAISコードが付与され、検索画面でコードを入力することで該当製品の詳細情報を確認できます。また、企業コードのみを入力することで、その企業が提供する全製品を一括で調べることも可能です。

### 福祉用具の分類コード (CCTA95)

TAISに登録された福祉用具には、6桁の分類コード (CCTA95) が付与されます。このコードは、用具の機能や目的に基づいて整理されており、以下のような階層構造を持ちます：
- **例:** 後輪駆動式車いす `122106`

分類コードは「大分類」「中分類」「小分類」の3段階で構成され、ISO9999との調和を図りつつ、日本独自の分類基準として制定されています。このコードにより、福祉用具の選択や使用方法に関する情報を体系的に提供します。

### 貸与価格の上限について

福祉用具の貸与価格には、商品価格のほか、計画書の作成や保守点検などの諸経費が含まれるため、事業者の裁量によって価格が大きく異なる場合があります。この課題に対応するため、全国的な貸与価格の状況を把握し、公表する仕組みが構築されました。

【貸与価格の公表について】  
[https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000212398.html](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000212398.html)

## 機能

### 福祉用具の全国平均貸与価格及び貸与価格の上限一覧のインポート

`TAIS+`モジュールでは、福祉用具の全国平均貸与価格および貸与価格の上限一覧をインポートする機能を提供します。この機能により、価格情報を効率的に管理し、Odoo内で利用可能にします。

- **インポートの流れ**  
  1. ユーザーが価格リストファイル（`.xlsx`形式）をアップロードします。
  2. ファイル名から日付情報を抽出し、価格リストのヘッダー情報を生成します。
  3. ファイル内のシートを解析し、指定されたヘッダー行を基にデータを読み取ります。
  4. 読み取ったデータをOdooの価格リストモデルに登録します。

- **対応するファイル形式**  
  - ファイル名は`pricelist_YYYY-MM-DD_○○.xlsx`または`pricelistYYYYMM.xlsx`の形式である必要があります。
  - ヘッダー行には以下の列が含まれている必要があります：
    - 商品コード
    - 法人名
    - 商品名
    - 型番
    - 全国平均貸与価格（円）
    - 貸与価格の上限（円）

- **エラーハンドリング**  
  - ファイル名やヘッダー行が期待される形式でない場合、適切なエラーメッセージを表示します。
  - インポート中にエラーが発生した場合、処理を中断せず、ログに記録します。

- **データの登録**  
  - 新しい価格リストが作成されるか、既存の価格リストが更新されます。
  - 各価格リストアイテムが関連付けられたモデルに登録されます。

詳細な実装については、以下のファイルを参照してください：
- `/opt/odoo/custom_addons/taisplus/models/pricelist_import.py`

### TAISコードの管理

`TAIS+`モジュールでは、Odooの製品モデルにTAISコードを管理する機能を追加しています。以下の機能を提供します：

- **TAISコードフィールドの追加**  
  製品テンプレートおよび製品バリアントに対して、`tais_code`フィールドを追加し、TAISコードを管理します。

- **製品タイプの拡張**  
  製品テンプレートに新しい詳細タイプ「福祉用具(TAIS)」を追加し、福祉用具を特定のカテゴリとして管理します。

- **TAISコードの計算と検索**  
  製品テンプレートとバリアント間でTAISコードを同期し、効率的な検索を可能にします。

- **ツールチップのカスタマイズ**  
  福祉用具タイプの製品に対して、特定のツールチップメッセージを表示します。

詳細な実装については、以下のファイルを参照してください：
- `./taisplus/models/product.py`

### 貸与価格の上限取得

`TAIS+`モジュールでは、特定のTAISコードと日付に基づいて貸与価格の上限を取得するAPIを提供しています。

- **モデルとメソッド**  
  - モデル: `taisplus.api.service`
  - メソッド: `get_tais_price_cap_json`

- **パラメータ**  
  - `tais_code` (文字列): TAISコード（形式: `01234-012345`）
  - `date_string` (文字列): 対象日付（形式: `yyyy-mm-dd`）

- **戻り値の例**  
  ```json
  {
    "tais_code": "01234-012345",
    "target_date": "2023-10-01",
    "target": {
      "name": "リスト名称x",
      "date": "2023-10-01",
      "average_price": "1000",
      "price_cap": "1111",
      "currency": "JPY",
    },
    "future": {
      "name": "リスト名称y",
      "date": "2025-04-01",
      "average_price": "1200",
      "price_cap": "2222",
      "currency": "JPY",
    },
  }
  ```

- **注意事項**  
  - 日付は`yyyy-mm-dd`形式である必要があります
  - 戻り値には`date_serializer`を使用して日付オブジェクトをシリアライズします
  - 対象となる価格一覧の情報が見つからない場合、`null`が設定されます

- **EXCEL VBAからの利用**  
  このAPIは、EXCELのVBAを使用しても利用可能です。[`odoo-json-rpc-vba`](https://github.com/jp-rad/odoo-json-rpc-vba)を使用して、貸与価格の上限を取得できます。以下はVBAでの簡単な例です：
  ```vba
  Sub GetPriceCap()
    Dim cl As New OdWebClient
    Dim args As New Collection
    Dim ret As OdResult
    Dim dic As Dictionary
    
    cl.SetInsecure True ' 自己証明書対策
    
    ' 接続情報
    cl.BaseUrl = "https://localhost"
    cl.DbName = "dev_odoo"
    cl.Username = "admin"
    cl.Password = "a123...999z"   ' 個人設定のAPIキー
    
    ' 認証
    cl.Common.Authenticate
    
    ' 取得
    args.Add "01234-012345" ' TAISコード
    args.Add "2023-10-01"   ' 日付（文字列）
    Set ret = cl.Model("taisplus.api.service").ExecuteKw("get_tais_price_cap_json", args)
    Debug.Print ret.JsonResult
    
    ' JSON文字列をDictionaryへ変換
    Set dic = JsonConverter.ParseJson(ret.JsonResult)

    ' 貸与価格の上限
    If IsNull(dic("target")) Then
        Debug.Print "貸与価格の上限：", "(なし)"
    Else
        Debug.Print "貸与価格の上限：", dic("target")("price_cap")
    End If
  End Sub
  ```

## インストール方法

1. リポジトリをOdooのカスタムアドオンディレクトリにクローンします:
   ```bash
   cd <カスタムアドオンディレクトリ>
   git clone https://github.com/jp-one/joo-tais-plus
   ```

2. odoo.confでaddons_pathにクローンしたディレクトリを追記します:
   ```text
   [options]
   http_interface = 0.0.0.0
   http_port = 8069
   #longpolling_port = 8072
   server_wide_modules = base,web
   data_dir = /opt/odoo/data
   list_db = False
   proxy_mode = True
   workers = 5
   addons_path = /opt/odoo/odoo/odoo/addons,/opt/odoo/odoo/addons
      ,/opt/odoo/custom_addons/joo-taisplus
   ```

3. Odooサーバーを再起動して新しいモジュールを検出します:
   ```bash
   sudo service odoo restart
   ```

4. Odooにログインし、アプリメニューに移動してアプリリストを更新します。

5. `TAIS+`モジュール (`tais_plus`) を検索してインストールします。

## 注意事項

`TAIS+`モジュール (`tais_plus`) は、福祉用具情報システム（TAIS）に準拠した機能を提供するため、福祉用具関連ビジネスに特化した設計となっています。モジュールの利用にあたっては、TAISコードや分類コードの正確な運用が求められます。特に貸与価格の上限においては、返戻（へんれい）の対象とならないようにするためにも、その確認を毎月行う運用が必要です。
