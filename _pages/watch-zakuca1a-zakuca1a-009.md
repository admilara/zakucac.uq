---
layout: default
title: KONČAR INEM - WATCH GEN A
---

### KONČAR INEM - WATCH LOG - AGREGAT A 

### UQ regulacija na sučelju s mrežom

#### Watch 009

Na grafovima niže prikazani su zapisi veličina dostavljeni od strane Končar INEM-a. 
Sve veličine su preuzete iz dostavljene log datoteke `watch-zakuca1a-zakuca1a-009.log`.
                               
Prikazane veličine su:
{% raw %}

<style scoped>
table {
  font-size: 13px;
}
</style>
| Signal | Jedinica | Opis |
|--------|----------|------|
| **VGACT** | [kV] | Napon generatora |
| **PACT** | [MW] | Radna snaga generatora |
| **QACT** | [Mvar] | Jalova snaga generatora |
| **VGREF** | [pu] | Referenca napona na generatoru |
| **PACTH** | [MW] | Radna snaga na sučelju |
| **QACTH** | [Mvar] | Jalova snaga na sučelju |
| **QHREF** | [Mvar] | Referenca jalove snage na sučelju |
| **VHACT** | [kV] | Napon na sučelju |
| **VHREF** | [kV] | Referenca napona na sučelju |
| **COSPHIH** | [pu] | Faktor snage na sučelju |
| **COSHREF** | [pu] | Referenca faktora snage na sučelju |
| **IFACT** | [A] | Struja uzbude |
| **UFACT** | [V] | Napon uzbude |
| **OEXLIMON** | [log16] | Aktivan limiter u naduzbudi (binarni signal) |
| **QACTHMAX** | [log16] | Granica maksimalne jalove snage na VN dosegnuta (binarni signal) |

{% endraw %}

<div class="wide-graph">
    <iframe src="{{ site.baseurl }}/watch-htmls-a/watch-zakuca1a-zakuca1a-009.html" width="100%" height="800px" frameborder="0"></iframe>
</div>
