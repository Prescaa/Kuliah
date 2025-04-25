package com.presca.modul2

import kotlin.math.ceil

object TipCalculator {
    fun calculateTip(cost: Double, percentage: Int, roundUp: Boolean): Double {
        var tip = cost * percentage / 100
        if (roundUp) tip = ceil(tip)
        return tip
    }
}
