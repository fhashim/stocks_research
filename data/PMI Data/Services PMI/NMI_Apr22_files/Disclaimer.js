﻿(function () {
    function initThisComponent() {
        new Vue({
            el: "#alert-modal-disclaimer",
            data: {
                disclaimerFlag: '0',
                modalShow: true,
                disclaimerClass: ['disclaimerClass']
            },
            mounted() {
                if (sessionStorage.disclaimerFlag) {
                    this.disclaimerFlag = sessionStorage.disclaimerFlag;
                }
            },
           
            watch: {
                disclaimerFlag(newDisclaimerFlag) {
                    sessionStorage.disclaimerFlag = newDisclaimerFlag;
                }
            }
        });
    }
    document.addEventListener("DOMContentLoaded", initThisComponent, false);
})();