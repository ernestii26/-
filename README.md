你好
===
1. $m' \equiv m r^e \ (mod{n})$
2. $s' \equiv (m')^d \ (mod{n})$
3. $s \equiv s'*r^{-1} \ (mod{n})$
4. $s^e \equiv m^{ed} \ (mod{n}) = m \ (mod{n})$
可以用RSA進行盲簽名的原因
$r^{ed} \equiv r\ (mod{n})$
$s \equiv s'*r^{-1} \equiv (m')^dr^{-1} \equiv m^{d}r^{ed}r^{-1} \equiv m^{d}r^{1}r^{-1} \equiv m^{d}r^{ed}r^{-1} \equiv m\ (mod{n})$

先運用數位簽名來驗證選票是本人投的並讓server運用盲簽名技術來為選票產生證明，但server端簽名的時候並不知道選票結果，之後回傳的時候不需要再給一次數位簽名，但是因為選票上面已經有server的盲簽名，因此可以知道選票是合法但不知道是誰投的以維持匿名性


首先匿名投票系統(server)運用RSA算法的generate key產生public key (e, n)及private key (d, n)
![image](https://hackmd.io/_uploads/rJPkMgXHC.png)
向投票人(client)公布其公鑰(e, n)
client也用RSA產生私鑰及公鑰並將公鑰的兩個變數當成name和id

client決定要投票的人m選擇一個blinding_factor，用公鑰(e, n)將 $m$ 加密為 $m'$ 在程式裡將 $m'$ 命名為encm
加入blinding factor是讓server端就算解密也無法知道投票結果m，運用 $m' \equiv m r^e \ (mod{n})$ 其中r為blinding factor


用client端生成的私鑰(digital_signature_private_key)將encm加密成checkencm並將(encm, checkencm, digital_signature_public_key)回傳給server端，server端會用數位簽名驗證選票是你投出的但看不選票m

接下來server端用他的私鑰(d, n)對選票encm進行盲簽名，得到signature
$s' \equiv (m')^d \ (mod{n})$ $s'$ 為你得到的signature $m'$ 為encm
```
def signfunc(private_key, blind_m):
    signature = pow(blind_m, private_key[0], private_key[1])
    return signature
```
並回傳signature到client端

client端用unblinding factor以及public key將signature unblinding獲得其選票結果m的憑證
$s \equiv s'*r^{-1} \ (mod{n})$ s為signature_unblind


將m和signature_unblind(s)傳給server，server會藉由signature_unblind驗證這張選票是被簽名過的，並將投票紀錄
用公式4$s^e \equiv m^{ed} \pmod{n} = m \ (mod{n})$
總結:
client 第一階段提供過name, id, encm, checkencm，或得憑證signature
第一階段未透露選票結果

client 第二階段提供voting result: m以及signature_unblind
第二階段未透露身分
在第二階段，client可以在和時間上傳，且不一定要用同一個機器上傳，因此server端僅可以驗證選票的正確性卻無法知道是誰投的

如何避免修改及重複投票，在第一階段時server可以紀錄誰簽名過，並過濾掉重複簽名者。

可以藉由同時執行server以及client交互作用來進行投票，其中client1的name 及 id固定，而client2則是隨機動態生成

