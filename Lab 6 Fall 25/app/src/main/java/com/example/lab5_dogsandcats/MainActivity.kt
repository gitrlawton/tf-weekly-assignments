package com.example.lab5_dogsandcats

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.codepath.asynchttpclient.AsyncHttpClient
import com.codepath.asynchttpclient.callback.JsonHttpResponseHandler
import okhttp3.Headers
import kotlin.random.Random

class MainActivity : AppCompatActivity() {
    private lateinit var petList: MutableList<String>
    private lateinit var rvPets : RecyclerView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        rvPets = findViewById<RecyclerView>(R.id.pet_list)
        petList = mutableListOf()
        fetchDogImages()
    }


    private fun fetchDogImages() {
        val client = AsyncHttpClient()

        client["https://dog.ceo/api/breeds/image/random/20", object : JsonHttpResponseHandler() {
            override fun onSuccess(statusCode: Int, headers: Headers, json: JsonHttpResponseHandler.JSON) {
                Log.d("Dog", "response successful: $json")
//                val petImageURL = json.jsonObject.getString("message")
//                Log.d("petImageURL", "pet image URL set: $petImageURL")

                val petImageArray = json.jsonObject.getJSONArray("message")

                for (i in 0 until petImageArray.length()) {
                    petList.add(petImageArray.getString(i))
                }

                val adapter = PetAdapter(petList)
                rvPets.adapter = adapter
                rvPets.layoutManager = LinearLayoutManager(this@MainActivity)
//                val imageView = findViewById<ImageView>(R.id.petImage)
//                Glide.with(this@MainActivity)
//                    .load(petImageURL)
//                    .fitCenter()
//                    .into(imageView)
            }

            override fun onFailure(
                statusCode: Int,
                headers: Headers?,
                errorResponse: String,
                throwable: Throwable?
            ) {
                Log.d("Dog Error", errorResponse)
            }
        }]
    }

    private fun fetchCatImage() {
        val client = AsyncHttpClient()

        client["https://api.thecatapi.com/v1/images/search", object : JsonHttpResponseHandler() {
            override fun onSuccess(statusCode: Int, headers: Headers, json: JsonHttpResponseHandler.JSON) {
                Log.d("Cat", "response successful: $json")
                var resultsJSON = json.jsonArray.getJSONObject(0)
                var petImageURL = resultsJSON.getString("url")
                Log.d("petImageURL", "pet image URL set: $petImageURL")

//                val imageView = findViewById<ImageView>(R.id.petImage)
//                Glide.with(this@MainActivity)
//                    .load(petImageURL)
//                    .fitCenter()
//                    .into(imageView)
            }

            override fun onFailure(
                statusCode: Int,
                headers: Headers?,
                errorResponse: String,
                throwable: Throwable?
            ) {
                Log.d("Cat Error", errorResponse)
            }
        }]
    }

}