package com.example.kk_commerce;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.Toast;
import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.ParsedRequestListener;
import com.example.kk_commerce.Models.Buyer;
import com.example.kk_commerce.Models.ResponseMessage;

import static com.example.kk_commerce.Constants.BASE_URL;

public class LogInActivity extends AppCompatActivity {
    Button signUp;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        signUp = findViewById(R.id.signup);
        signUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent in = new Intent(LogInActivity.this, RegistrationActivity.class);
                startActivity(in);
            }
        });
    }

    public void SignIn(String username, String password){
        AndroidNetworking.post(BASE_URL + "/signin")
                .addBodyParameter("username", username).addBodyParameter("password", password)
                .setTag("test").setPriority(Priority.MEDIUM).build()
                .getAsObject(Buyer.class, new ParsedRequestListener<Buyer>(){
                    @Override
                    public void onResponse(Buyer buyer) {
                        ResponseMessage response = buyer.getResponse();
                        if (response.getMessage().equals("Login Successful")){
                            Log.i("conn", ""+buyer.getId());
                            Intent intent = new Intent(getApplicationContext(), DashboardActivity.class);
                            SharedPreferences preferences = getApplicationContext().getSharedPreferences("User", MODE_PRIVATE);
                            SharedPreferences.Editor editor = preferences.edit();
                            editor.putInt("Buyer", Integer.parseInt(buyer.getId()));
                            editor.apply();
                            intent.putExtra("name", buyer.getFirst_name());
                            Toast.makeText(LogInActivity.this, "Welcome", Toast.LENGTH_LONG).show();
                            startActivity(intent);
                        }else {
                            Toast.makeText(LogInActivity.this, ""+ response.getMessage(), Toast.LENGTH_LONG).show();
                        }
                    }
                    @Override
                    public void onError(ANError error) {
                        Log.i("conn", ""+ error);
                        if(error.getErrorCode() == 0){
                            Toast.makeText(LogInActivity.this, "Network Error", Toast.LENGTH_LONG).show();
                        }
                    }
                });
    }
}