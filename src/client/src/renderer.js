$(function() {

    command_list = {
        START: '!START',
        STOP: '!STOP',
        SEND_TRADER_INFO: '!SEND_TRADER_INFO',
        SEND_WALLET_INFO: '!SEND_WALLET_INFO',
        SET_TRADER_INFO: '!SET_TRADER_INFO',
        SET_WALLET_INFO: '!SET_WALLET_INFO',
        BROADCAST: '!BROADCAST',
        PING: '!PING', 
        NONE: '!NONE',
        GET_ALL: '!GET_ALL',
    }

    // Creating a new socket connection to the server 
    const websocket = new WebSocket('ws://127.0.0.1:5050/');

    // Setting the socket event listeners
    websocket.addEventListener('open', socket_open_handle);
    websocket.addEventListener('message', socket_message_handle);
    websocket.addEventListener('close', socket_close_handle);
    websocket.addEventListener('error', socket_error_handle);
    
    // Setting the event listener for the trader settings save button
    $('#save-trader-settings').on('click', () => {
        data = {
            command: command_list.SET_TRADER_INFO,
            trader_info: {
                discard_buy_point: $('#discard_buy_point').val(),
                discard_sell_point: $('#discard_sell_point').val(),
                new_buy_point: $('#new_buy_point').val(),
                new_sell_point: $('#new_sell_point').val(),
                buy_coefficient: $('#buy_coefficient').val(),
                sell_coefficient: $('#sell_coefficient').val(),
                manual_buy_point: $('#manual_buy_point').val(),
                manual_sell_point: $('#manual_sell_point').val(),
                max_buy_point: $('#max_buy_point').val(),
                max_gas_fees: $('#max_gas_fees').val()
            }
        }

        websocket.send(JSON.stringify(data));
    });
});