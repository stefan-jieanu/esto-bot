function ui_set_trader_info(data) {
    // Trader stats
    $('#current_traded_coint_price').val(data['current_traded_coint_price'])
    $('#moving_average_high').val(data['moving_average_high'])
    $('#moving_average_low').val(data['moving_average_low'])
    $('#ten_day_moving_average_high').val(data['ten_day_moving_average_high'])
    $('#ten_day_moving_average_low').val(data['ten_day_moving_average_low'])
    $('#high_coefficient').val(data['high_coefficient'])
    $('#low_coefficient').val(data['low_coefficient'])
    $('#buy_point').val(data['buy_point'])
    $('#sell_point').val(data['sell_point'])

    // Trader settings
    $('#discard_buy_point').val(data['discard_buy_point'])
    $('#discard_sell_point').val(data['discard_sell_point'])
    $('#new_buy_point').val(data['new_buy_point'])
    $('#new_sell_point').val(data['new_sell_point'])
    $('#buy_coefficient').val(data['buy_coefficient'])
    $('#sell_coefficient').val(data['sell_coefficient'])
    $('#manual_buy_point').val(data['manual_buy_point'])
    $('#manual_sell_point').val(data['manual_sell_point'])
    $('#max_buy_point').val(data['max_buy_point'])
    $('#max_gas_fees').val(data['max_gas_fees'])
}

function ui_set_wallet_info(data) {

}