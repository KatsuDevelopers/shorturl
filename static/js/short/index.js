window.addEventListener('DOMContentLoaded', () => {
    const appearSuccess = (shortenedURL) => {
        let success = $('#success')
        success.attr("href", shortenedURL)
        success.text(shortenedURL)
    }
    const clearForm = (form) => {
        form.find('input[name="original"]').val('')
        form.find('input[name="alias"]').val('')
    }
    const showError = ({responseJSON}) => {
        $('#error').text(`Error ${JSON.stringify(responseJSON)}`)
    }

    $(document).ready(() => {
        $('input[name=auto_generate]').change(function() {
            if ($(this).is(':checked')){
                $('#alias').css('visibility', 'hidden')
                $('#alias_div').css('visibility', 'hidden')
                $('#alias_label').css('visibility', 'hidden')
                $('#alias').val("")
            } else {
                $('#alias').css('visibility', 'visible')
                $('#alias_div').css('visibility', 'visible')
                $('#alias_label').css('visibility', 'visible')
            }
        })
    });

    (() => {
        let urlForm = $('#url_short')
        urlForm.submit((e) => {
            e.preventDefault()
            let original = urlForm.find('input[name="original"]').val()
            let alias = urlForm.find('input[name="alias"]').val()
            let auto = urlForm.find('input[name=auto_generate]').is(':checked')
            let data = {
                'url_name': alias,
                'original': original,
                'auto': auto
            }
            data = JSON.stringify(data)
            console.log(data)
            let url = `/api/url-short/`
            $.ajax({
                type: 'POST',
                url: url,
                Accept: "application/json",
                contentType: "application/json",
                headers: {
                    'X-CSRFToken': '{{csrf_token}}'
                },
                data: data,
                success: (response) => {
                    appearSuccess(response.alias)
                    clearForm(urlForm)
                },
                error: (XMLHttpRequest, textStatus, errorThrown) => {
                    console.log(XMLHttpRequest)
                    showError(XMLHttpRequest)
                    console.log(textStatus)
                    console.log(errorThrown)
                }
            })
        })
    })();
})