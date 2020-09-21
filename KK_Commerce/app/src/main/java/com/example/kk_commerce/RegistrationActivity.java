package com.example.kk_commerce;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.ParsedRequestListener;
import com.example.kk_commerce.Models.Token;
import com.google.android.material.textfield.TextInputEditText;

import static com.example.kk_commerce.Constants.BASE_URL;

public class RegistrationActivity extends AppCompatActivity {
    TextInputEditText txtPassword, txtEmail, txtFisrtName, textLastName;
    Button signUpBtn, signIn;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registration);

        signIn = findViewById(R.id.signin);
        signIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent in = new Intent(RegistrationActivity.this, LogInActivity.class);
                startActivity(in);
            }
        });
    }

    public void SignUp(String username, String email, String password, String first_name, String last_name, String gender){
        AndroidNetworking.post(BASE_URL + "/signup")
                .addBodyParameter("username", username)
                .addBodyParameter("password", password)
                .addBodyParameter("email", email)
                .addBodyParameter("first_name", first_name)
                .addBodyParameter("last_name", last_name)
                .addBodyParameter("gender", gender)
                .setTag("test")
                .setPriority(Priority.MEDIUM)
                .build()
                .getAsObject(Token.class, new ParsedRequestListener<Token>(){
                    @Override
                    public void onResponse(Token token) {
                        Intent intent = new Intent(getApplicationContext(), DashboardActivity.class);
                        SharedPreferences preferences = getApplicationContext().getSharedPreferences("User", MODE_PRIVATE);
                        SharedPreferences.Editor editor = preferences.edit();
                        editor.putString("token", token.getToken());
                        editor.apply();
                        Toast.makeText(RegistrationActivity.this, "User created successfully", Toast.LENGTH_LONG).show();
                        startActivity(intent);
                    }
                    @Override
                    public void onError(ANError error) {
                        Log.i("conn", ""+ error);
                        if(error.getErrorCode() == 0){
                            Toast.makeText(RegistrationActivity.this, "Network Error", Toast.LENGTH_LONG).show();
                        }
                    }
                });
    }
}