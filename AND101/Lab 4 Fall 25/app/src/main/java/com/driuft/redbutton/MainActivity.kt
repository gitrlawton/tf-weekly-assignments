package com.driuft.redbutton

import android.content.Intent
import android.content.SharedPreferences
import android.content.res.ColorStateList
import android.os.Bundle
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.driuft.redbutton.databinding.ActivityMainBinding
import com.driuft.redbutton.ui.FinalActivity
import es.dmoral.toasty.Toasty

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private val redButton get() = binding.redButton
    private val blueButton get() = binding.blueButton
    private val tinyYellowButton get() = binding.tinyYellowButton

    private val sharedPref: SharedPreferences by lazy {
        getPreferences(MODE_PRIVATE)
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        configureUI()
        configureToasty()
        setupClickListeners()
    }

    private fun setupClickListeners() {
        redButton.setOnClickListener { congratulations() }
        blueButton.setOnClickListener { blueButtonClicked() }
        tinyYellowButton.setOnClickListener { tinyButtonClicked() }
        tinyYellowButton.setOnLongClickListener { tinyButtonLongClicked() }
    }

    /**
     * Show a clue when the [blueButton] is clicked.
     */
    private fun blueButtonClicked() {
        // Reveal true color
        blueButton.setBackgroundColor(resources.getColor(R.color.blue))

        // Save state
        with (sharedPref.edit()) {
            putBoolean(getString(R.string.blue_button_shown_key), true)
            apply()
        }

        // Update color
        configureUI()

        Toasty.info(
            this,
            getString(R.string.toast_wrong_button_error),
            Toasty.LENGTH_LONG
        ).show()
    }

    /**
     * Shows a clue when the [tinyYellowButton] is clicked.
     */
    private fun tinyButtonClicked() {
        Toasty.warning(
            this,
            getString(R.string.toast_do_not_press_and_hold),
            Toasty.LENGTH_LONG
        ).show()
    }

    /**
     * [tinyYellowButton] was held
     * I wonder what will happen next...
     */
    private fun tinyButtonLongClicked(): Boolean {
        // Save state
        with (sharedPref.edit()) {
            putBoolean(getString(R.string.red_button_shown_key), true)
            apply()
        }

        // Update visibility
        configureUI()

        // TODO: MAKE THE RED BUTTON CLICKABLE
        redButton.isClickable = true

        return true
    }

    /**
     * Something is preventing me from clicking...
     * Maybe I should check out [R.layout.activity_main] to look for anything suspicious.
     */


    /**
     * Congratulations!!!
     * You DID it! The [redButton] seems pleased with your performance.
     */
    private fun congratulations() {
        val partyEmoji = String(Character.toChars(0x1F389))
        Toasty.success(
            this,
            getString(R.string.toast_congrats, partyEmoji),
            Toasty.LENGTH_LONG
        ).show()

        // Navigate to new activity to CELEBRATE!
        val i = Intent(this, FinalActivity::class.java)
        startActivity(i)
        finish()
    }

    /**
     * Configures UI and visibility of [blueButton] and [redButton] using [SharedPreferences].
     */
    private fun configureUI() {
        // Default value for SharedPreferences
        val defaultValue = false
        val redColor = resources.getColor(R.color.red)
        val blueColor = resources.getColor(R.color.blue)
        val blueButtonShown = sharedPref.getBoolean(getString(R.string.blue_button_shown_key), defaultValue)
        val redButtonShown = sharedPref.getBoolean(getString(R.string.red_button_shown_key), defaultValue)

        // Only update the color of the Blue button if it is visible
        if (blueButton.visibility == View.VISIBLE) {
            if (!blueButtonShown) {
                blueButton.backgroundTintList = ColorStateList.valueOf(redColor)
            } else {
                blueButton.backgroundTintList = ColorStateList.valueOf(blueColor)
            }
        }

        if (redButtonShown) {
            tinyYellowButton.visibility = View.GONE
            redButton.visibility = View.VISIBLE
        }
    }

    /**
     * Configures [Toasty] to not allow multiple Toasts to be queued.
     */
    private fun configureToasty() {
        Toasty.Config.getInstance()
            .allowQueue(false)
            .apply()
    }
}