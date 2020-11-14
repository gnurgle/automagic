let year_select = document.getElementById('year');
let make_select = document.getElementById('make');
let model_select = document.getElementById('model');
let trim_select = document.getElementById('trim');

        year_select.onchange = function() {
            year = year_select.value;
            fetch('/' + year + '/make/model/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let make of data.makes){
                        optionHTML += '<option value="' + make + '">' + make + '</option>';
                    }
                    make_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let model of data.models){
                        optionHTML += '<option value="' + model + '">' + model + '</option>';
                    }
                    model_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }

        make_select.onchange = function() {
            year = year_select.value;
            make = make_select.value;
            fetch('/' + year + '/'+ make +'/model/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let model of data.models){
                        optionHTML += '<option value="' + model + '">' + model + '</option>';
                    }
                    model_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }
        model_select.onchange = function() {
            year = year_select.value;
            make = make_select.value;
            model = model_select.value;

            fetch('/' + year + '/'+ make +'/'+ model +'/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }
