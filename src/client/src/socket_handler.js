function socket_open_handle(e) {
    
}

function socket_message_handle(e) {
    data = JSON.parse(e.data)

    if (data.hasOwnProperty('trader_info'))
        ui_set_trader_info(data['trader_info'])
    if (data.hasOwnProperty('traded'))
        alert('Trade happened!');
}

function socket_close_handle(e) {
    
}

function socket_error_handle(e) {
    console.log(e)
}
