package com.example.kk_commerce;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.ParsedRequestListener;
import com.example.kk_commerce.Adapters.OrderAdapter;
import com.example.kk_commerce.Adapters.OrderProductAdapter;
import com.example.kk_commerce.Fragments.OrdersFragment;
import com.example.kk_commerce.Models.Order;
import com.example.kk_commerce.Models.Product;
import com.example.kk_commerce.Models.Token;

import java.util.List;

import static com.example.kk_commerce.Constants.BASE_URL;

public class OrderDetailsActivity extends AppCompatActivity implements OrderProductAdapter.ItemListener {
    String m_token;
    AlertDialog.Builder builder;
    TextView text_username, text_password;
    OrderProductAdapter adapter;
    RecyclerView recyclerView;
    RecyclerView.LayoutManager RecyclerViewLayoutManager;
    String order_id;
    Toolbar toolbar;
    TextView pageTitle;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_order_details);

        toolbar = (Toolbar) findViewById(R.id.toolbar);
        toolbar.setBackgroundColor(getResources().getColor(R.color.colorWhiteTrans));
        setSupportActionBar(toolbar);
        pageTitle = (TextView) toolbar.findViewById(R.id.tv_title);
//        pageTitle.setText("COMMERCE");
        pageTitle.setTextColor(getResources().getColor(R.color.primaryDarkColor));
        getSupportActionBar().setTitle("COMMERCE");

        recyclerView = findViewById(R.id.recyclerView);
        RecyclerViewLayoutManager = new LinearLayoutManager(OrderDetailsActivity.this);
        recyclerView.setLayoutManager(RecyclerViewLayoutManager);

        SharedPreferences preferences = getSharedPreferences("User", MODE_PRIVATE);
        m_token = String.valueOf(preferences.getString("token", "1"));
        Intent intent = getIntent();
        order_id = intent.getStringExtra("order_id");


        if (! m_token.equals("1")){
            get_data(m_token, order_id);
        }else {
            getDialog();
        }
    }

    @Override
    public void onItemClick(Product product) {
//        Intent in = new Intent(getActivity(), OrderDetailsActivity.class);
//        in.putExtra("order_id", order.getId());
//        startActivity(in);
    }

    public void get_data(String token, String order_id){
        AndroidNetworking.get( BASE_URL + "order/products/"+order_id)
                .setTag("Orders")
                .addHeaders("Authorization","Token " + token)
                .setPriority(Priority.LOW)
                .build()
                .getAsObjectList(Product.class, new ParsedRequestListener<List<Product>>(){
                    @Override
                    public void onResponse(List<Product> products) {
                        adapter = new OrderProductAdapter(OrderDetailsActivity.this, products, OrderDetailsActivity.this);
                        recyclerView.setAdapter(adapter);
                    }

                    @Override
                    public void onError(ANError anError) {
                        Toast.makeText(OrderDetailsActivity.this, "" + anError.getErrorBody() + anError.getMessage() + anError.getResponse(), Toast.LENGTH_LONG).show();
                    }
                });
    }

    public void getDialog() {
        builder = new AlertDialog.Builder(OrderDetailsActivity.this);
        LayoutInflater inflater = getLayoutInflater();

        View mView = inflater.inflate(R.layout.dialog_signin, null);
        text_username = mView.findViewById(R.id.username);
        text_password = mView.findViewById(R.id.password);

        builder.setView(mView)
                // Add action buttons
                .setPositiveButton("LogIn", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        String username = text_username.getText().toString().trim();
                        String password = text_password.getText().toString().trim();
                        login(username, password, dialog);
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.dismiss();
                    }
                });

        AlertDialog alertDialog = builder.create();
        alertDialog.show();
    }
    public void login(String username, String password, final DialogInterface dialogInterface){
        AndroidNetworking.post(BASE_URL + "login")
                .addBodyParameter("consumer_key", username)
                .addBodyParameter("consumer_password", password)
                .setTag("test")
                .setPriority(Priority.MEDIUM)
                .build()
                .getAsObject(Token.class, new ParsedRequestListener<Token>(){
                    @Override
                    public void onResponse(Token token) {
                        SharedPreferences preferences = getSharedPreferences("User", MODE_PRIVATE);
                        SharedPreferences.Editor editor = preferences.edit();
                        editor.putString("token", token.getToken());
                        editor.apply();
                        m_token = token.getToken();
                        dialogInterface.dismiss();
                    }
                    @Override
                    public void onError(ANError error) {
                        Log.i("conn", ""+ error);
                        if(error.getErrorCode() == 0){
                            Toast.makeText(OrderDetailsActivity.this, "Network Error", Toast.LENGTH_LONG).show();
                        }
                    }
                });
    }
}