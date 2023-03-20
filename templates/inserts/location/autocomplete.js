var autocompleteTimer;
    $('.addressAutoComplete').autoComplete({
        resolver: 'custom',
        minLength: 5,
        events: {
            search: function (qry, callback) {
                clearTimeout(autocompleteTimer)
                autocompleteTimer = setTimeout(function() {
                    let header = new Headers({'content-type': 'application/json'});
                    fetch("/locationAutocomplete", {method: "POST", body: JSON.stringify({"address" : qry}), headers: header})
                        .then(res => res.text())
                        .then(response => {
                            let resp = JSON.parse(response);
                            let ans = []
                            for (result of resp["results"]) {
                                ans.push(result["formatted"])
                            }
                            callback(ans)
                        });
                }, 1000);
            }

        }
    });