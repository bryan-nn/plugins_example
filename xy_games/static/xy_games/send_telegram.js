(function(){
        $.atoms.telegram_custom = [
            {
                tag_code: "text_input",
                type: "textarea",
                attrs: {
                    name: gettext("内容"),
                    placeholder: gettext("发送信息"),
                    hookable: true,
                    validation: [
                        {
                            type: "required"
                        }
                    ]
                }
            },
            {
                tag_code: "receiver_input",
                type: "textarea",
                attrs: {
                    name: gettext("收件人"),
                    placeholder: gettext("收件人逗号分隔"),
                    hookable: true,
                    validation: [
                        {
                            type: "required"
                        }
                    ]
                }
            }
        ]
    })();