var autocompleteTimer;
    $('.addressAutoComplete').autoComplete({
        resolver: 'custom',
        minLength: 5,
        events: {
            search: function (qry, callback) {
                clearTimeout(autocompleteTimer)
                autocompleteTimer = setTimeout(function() {
                    let header = new Headers({'content-type': 'application/json'});
                    fetch("/location/autocomplete", {method: "POST", body: JSON.stringify({"address" : qry}), headers: header})
                        .then(res => res.text())
                        .then(response => {
                            let resp = JSON.parse(response);
                            let ans = []
                            for (result of resp["results"]) {
                                if (result["rank"]["confidence"] <= 0.5) {
                                    continue
                                }
                                if (result["address_line1"].split('—').length-1 > 0){
                                    continue
                                }
                                if (typeof result["street"] === 'undefined'){
                                    continue
                                }
                                let temp = "";
                                if ("city" in result) {
                                    temp += result["city"];
                                }
                                else {
                                    temp += result["county"]
                                }
                                temp += ", " + result["street"]
                                if ("housenumber" in result){
                                    temp += " " + result["housenumber"]
                                }
                                ans.push(temp)
                            }
                            trueAns = []
                            for (checkedAns in ans){
                                let isAdded = false
                                for (currentAns in trueAns){
                                    if (trueAns[currentAns].valueOf() === ans[checkedAns].valueOf()) {
                                        isAdded = true;
                                        break;
                                    }
                                }
                                if (!isAdded){
                                    trueAns.push(ans[checkedAns])
                                }
                            }
                            if (trueAns.length !== 0) {
                                callback(trueAns)
                            }
                        });
                }, 1000);
            }

        }
    });