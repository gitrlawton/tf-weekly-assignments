package com.driuft.redbutton.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.driuft.redbutton.R
import com.driuft.redbutton.databinding.ActivityFinalBinding
import com.driuft.redbutton.util.Konfigs
import nl.dionsegijn.konfetti.xml.KonfettiView

/**
 * This activity CELEBRATES what an amazing engineer you are!
 * If you got to this point, that means you have successfully debugged the app to completion.
 * You should be proud!
 */
class FinalActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFinalBinding
    private lateinit var konfetti: KonfettiView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFinalBinding.inflate(layoutInflater)
        konfetti = binding.konfettiView
        setContentView(binding.root)

        val heartEmoji = String(Character.toChars(0x2764))
        binding.madeWithLoveText.text = getString(R.string.made_with_love_text, heartEmoji)
        binding.trophy.setOnClickListener { itsPartyTime() }

        itsPartyTime()
    }

    /**
     * See [Konfigs] in the .util package for confetti configurations
     */
    private fun itsPartyTime() {
        konfetti.start(Konfigs.festive())
        konfetti.start(Konfigs.explode())
        konfetti.start(Konfigs.parade())
        konfetti.start(Konfigs.rain())
    }
}