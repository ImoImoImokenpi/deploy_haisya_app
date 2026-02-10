function checkForm() {
    // fieldのチェック
    var driverFields = document.getElementsByClassName("driver-field");
    for (var i = 0; i < driverFields.length; i++) {
        var name = driverFields[i].querySelector("input[name^='driver'][name$='[name]']").value;
        if (name.trim() === "") {
            alert("Please fill in all driver fields.");
            // driverfieldがi回終われば、送信される
            return false;
        }
    }

    // fieldのチェック
    var passengerFields = document.getElementsByClassName("passenger-field");
    for (var i = 0; i < passengerFields.length; i++) {
        var name = passengerFields[i].querySelector("input[name^='passenger'][name$='[name]']").value;
        if (name.trim() === "") {
            alert("Please fill in all passenger fields.");
            // driverfieldがi回終われば、送信される
            return false;
        }
    }

    // フォーム送信
    return true;
}

function checkNaming() {
    // fieldのチェック
    var namingField = document.querySelector("input[name='history[name]']");
    var naming = namingField.value.trim();
    if (naming === "") {
        alert("履歴名を入力してください。");
        return false;
    }
    return true;
}


function copyText() {
    // コピーするテキストを取得
    var resultArea = document.getElementById("resultArea")
    
    var textToCopy = "";

    var drivers = resultArea.querySelectorAll('.card-title');
    drivers.forEach(function(driverElement) {
        // ドライバー名を取得
        var driverName = driverElement.innerText;
        var beforeSlash_d = driverName.split("/")[0];
        // 乗客リストを取得
        var passengerList = driverElement.nextElementSibling.getElementsByTagName("li");
        var passengersText = "";
        for (var i = 0; i < passengerList.length; i++) {
            var fullText = passengerList[i].innerText;
            var beforeSlash_p = fullText.split("/")[0];
            passengersText += beforeSlash_p + "\n";
        }
        // ドライバー名と乗客リストを結合
        textToCopy += beforeSlash_d + "車" + ":\n" + passengersText + "\n";
    });

    var tempTextArea = document.createElement("textarea");
    tempTextArea.value = textToCopy;
    tempTextArea.style.position = "fixed"; // 要素が画面外に行かないように
    document.body.appendChild(tempTextArea);
    // テキストエリアを選択し、コピー
    tempTextArea.select();
    document.execCommand("copy");
    // 不要なテキストエリアを削除
    document.body.removeChild(tempTextArea);
    // ユーザーにコピーされた旨を通知する（任意）
    alert("配車結果がクリップボードにコピーされました。");
}

function copyUrl() {
    var currentURL = window.location.href; // 現在のURLを取得
    navigator.clipboard.writeText(currentURL); // URLをクリップボードにコピー
    alert("クリップボードにURLがコピーされました: " + currentURL); // コピーされたことを通知
}