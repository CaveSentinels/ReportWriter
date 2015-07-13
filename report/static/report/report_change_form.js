jQuery(function() {

    window.onload=function() {
        // Hide the misuse cases and use cases fields on page load
        $("#muo-container").hide();
        $('#custom-muo-container').hide();

        // Apply the Select2 css to the CWE select field
        //$(".cwe-select-multiple").select2({
        //    placeholder: "Either click 'Suggest CWEs' to get the suggest CWE based on your description or select a CWE from the list"
        //});

        $(".cwe-select-multiple").select2({
                placeholder: "Either click 'Suggest CWEs' to get the suggest CWE based on your description or select a CWE from the list",
            ajax: {
                //url: "http://puppygifs.tumblr.com/api/read/json",
                url: "http://www.flickr.com/services/feeds/photos_public.gne?tags=soccer&format=json",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                  return {
                      q: params.term // search term
                      //page: params.page
                  };
                },

                processResults: function (data, page) {
                  // parse the results into the format expected by Select2.
                  // since we are using custom formatting functions we do not need to
                  // alter the remote JSON data
                  return {
                    results: data
                  };
                },
                cache: true
            },

            //escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
            minimumInputLength: 0,
            //templateResult: formatRepo, // omitted for brevity, see the source of this page
            //templateSelection: formatRepoSelection // omitted for brevity, see the source of this page
        });
    };






    $("body").on('click', '#cwe-suggestion-button', function(e){
        //TODO: Get the remote data here
        //load_cwes();
    });


    $("body").on('click', '#misusecase-suggestion', function(e){
        // Show the muo selection container with pre-populated misuse case related to the cwes. Also hide the custom
        // MUO creation form
        e.preventDefault();
        load_misusecases([]);
        $('#custom-muo-container').hide();
        $('#muo-container').show();
    });

    $("body").on('click', '#misusecase-custom', function(e){
        // Show the muo creation div. Also hide the muo selection container
        e.preventDefault();
        $('#muo-container').hide();
        $('#custom-muo-container').show();
    });

    $("body").on('click', '#muo-close', function(e){
        // Hide the muo selection container
        e.preventDefault();
        $('#muo-container').hide();
    });

    $("body").on('click', '#muo-select', function(e){
        e.preventDefault();

        // Get the selected misuse case and use case divs
        var selected_misuse_case_div = $('.misuse-case-container.selected');
        var selected_use_case_div = $('.use-case-container.selected');

        if (selected_misuse_case_div == undefined && selected_use_case_div == undefined) {
            // No misuse case and use case is selected
            alert('You should select at least a misuse case or close the suggested one and write your own misuse ' +
                  'case and use case')
        }
        else if (selected_misuse_case_div != undefined && selected_use_case_div == undefined) {
            // Misuse case is selected but no use case is selected
            alert('You have only selected a misuse case. Are you sure you want to write your own use case?');
        }
        else {
            // Misuse case and use case is selected

            // Get the custom muo container div
            $('#misusecase-description').val(selected_misuse_case_div.find('.misuse-case-div').text().trim());
            $('#usecase-description').val(selected_use_case_div.find('.use-case-div').text().trim());
            $('#osr-description').val(selected_use_case_div.find('.osr-div').text().trim());

            // Hide the muo selection container and show the muo creation div with all the fields disabled
            $('#muo-container').hide();
            $('#custom-muo-container').show();
        }
    });

    $("body").on('click', '.misuse-case-container', function(){
        // get the misuse case id of the clicked misuse case
        var misuse_case_id = $(this).attr("data-value");

        // get the misuse case id of the last selected misuse case
        var last_selected_misuse_case_id = $('.misuse-case-container.selected').attr("data-value");

        // If the selected misuse case is clicked again, do nothing, otherwise send the ajax
        // request to get the use cases corresponding to the clicked misuse case
        if (misuse_case_id != last_selected_misuse_case_id) {
            // Remove the selection from the last selected misuse case div
            $('.misuse-case-container.selected').removeClass('selected');

            // Select the current div
            $(this).addClass('selected');

            // Load usecases corresponding to the selected misuse
            load_usecases(misuse_case_id);
        }
    });

    $("body").on('click', '.use-case-container', function(){
        // get the use case id of the clicked misuse case
        var use_case_id = $(this).attr("data-value");

        // get the use case id of the last selected use case
        var last_selected_use_case_id = $('.use-case-container.selected').attr("data-value");

        // If the selected use case is clicked again, do nothing, otherwise add the css to the currently
        // selected use case
        if (use_case_id != last_selected_use_case_id) {
            // Remove the selection from the last selected misuse case div
            $('.use-case-container.selected').removeClass('selected');

            // Select the current div
            $(this).addClass('selected');
        }
    });

    $("input[name='osr-pattern']").change(function(){
        // Set the placeholder based on the selection
        var value = $(this).val();
        set_placeholder(value);
    });
});


//function load_cwes(description) {
//    if (description == null || description == '') {
//        // If description is None or Empty string, it means that either page has loaded for the first time or
//        // user had clicked 'Suggest CWEs' button without writing any description for the report.
//        $('#cwe-selection').replaceWith('');
//    }
//    else {
//        // Description is present, we need to make a call to the Enhanced CWE application to get the related CWEs
//        $.ajax({
//            url: 'report_report_cwes/',
//            type: 'POST',
//            data: {},
//
//            success: function (result) {
//                $('#cwe-selection').replaceWith(result);
//
//                alert("Hello" + result);
//
//                //var data =  [{ id: 0, text: 'CWE:123 Authentication Bypass by Alternate Name' },
//                //    { id: 1, text: 'CWE:456 Authentication Bypass by Spoofing' },
//                //    { id: 2, text: 'CWE:789 Buffer Overflow' },
//                //    { id: 3, text: 'CWE:086 Authentication Bypass by Alternate Name' },
//                //    { id: 4, text: 'CWE:256 Invalid Filed Traversal' }]
//
//                $(".cwe-select-multiple").select2({
//                    data: data
//                });
//
//            },
//
//            error: function (xhr, errmsg, err) {
//                alert("Oops! We have encountered and error \n" + errmsg);
//            }
//        });
//    }
//}


function load_misusecases(cwe_ids) {
    $.ajax({
        url: 'report_report_misusecases/',
        type: 'POST',
        data: {cwe_ids: cwe_ids}, // Send the selected CWE ids

        success: function(result) {
            $('.slim-scroll-div').replaceWith(result);
        },

        error: function (xhr,errmsg,err) {
            alert("Oops! We have encountered and error \n" + errmsg);
        }
    });
}


function load_usecases(misuse_case_id) {
    $.ajax({
        url: 'report_report_usecases/',
        type: 'POST',
        data: {misuse_case_id: misuse_case_id}, // Send the selected misuse case id

        success: function(result) {
            // If ajax call is successful, reload the fat-scroll-div which contains the use cases
            $('.fat-scroll-div').replaceWith(result);
        },

        error: function(xhr,errmsg,err) {
            // Show error message in the alert
            alert("Oops! We have encountered and error \n" + errmsg);
        }
    });
}


function set_placeholder(value) {
    var placeholder = 'Please write the requirements in the following format:\n';
    var addendum;
    switch(parseInt(value)) {
        case 1:
            addendum = "The <system name> shall <system response>\n\n" +
                                "Example: The software shall be written in Java";
            break;
        case 2:
            addendum = "WHEN <trigger> <optional precondition> the <system name> shall <system respons>\n\n" +
                                "Example: When a DVD is inserted into the DVD player, the OS shall spin up the optical drive";
            break;
        case 3:
            addendum = "IF <unwanted condition or event>, THEN the <system name> shall <system response>\n\n" +
                                "Example: If the memory checksum is invalid, then the software shall display an error message";
            break;
        case 4:
            addendum = "WHILE <system state>, the <system name> shall <system response>\n\n" +
                                "Example: While the heater is on, the software shall close the water intake valve";
            break;
        default:
            addendum = '';
    }
    placeholder = placeholder.concat(addendum);

    // Set the placeholder of the OSR text area
    $('#osr-description').attr("placeholder", placeholder);
}