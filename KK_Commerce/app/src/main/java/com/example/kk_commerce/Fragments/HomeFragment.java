package com.example.kk_commerce.Fragments;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.ParsedRequestListener;
import com.example.kk_commerce.Adapters.ProductAdapter;
import com.example.kk_commerce.DashboardActivity;
import com.example.kk_commerce.Models.Product;
import com.example.kk_commerce.ProductDetailActivity;
import com.example.kk_commerce.R;

import java.util.List;

import static com.example.kk_commerce.Constants.BASE_URL;

public class HomeFragment extends Fragment implements ProductAdapter.ItemListener {

    ProductAdapter adapter;
    RecyclerView recyclerView;
    GridLayoutManager manager;

    public HomeFragment() {

    }


    public static HomeFragment newInstance() {
        HomeFragment fragment = new HomeFragment();
        Bundle args = new Bundle();
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home2, container, false);
        recyclerView = view.findViewById(R.id.recyclerView);
        manager = new GridLayoutManager(getActivity(), 2, GridLayoutManager.VERTICAL, false);
        recyclerView.setLayoutManager(manager);
        get_data();
        return view;
    }

    public void get_data(){
        AndroidNetworking.get( BASE_URL + "products")
                .setTag("Products")
                .setPriority(Priority.LOW)
                .build()
                .getAsObjectList(Product.class, new ParsedRequestListener<List<Product>>(){
                    @Override
                    public void onResponse(List<Product> products) {
                        adapter = new ProductAdapter(getContext(), products, HomeFragment.this);
                        recyclerView.setAdapter(adapter);
                    }

                    @Override
                    public void onError(ANError anError) {
                        Toast.makeText(getContext(), "" + anError.getErrorBody() + anError.getMessage() + anError.getResponse(), Toast.LENGTH_LONG).show();
                    }
                });
    }

    @Override
    public void onItemClick(Product product) {
//        Toast.makeText(getContext(), product.getName() + " is clicked", Toast.LENGTH_SHORT).show();
        Intent i = new Intent(getActivity(), ProductDetailActivity.class);
        i.putExtra("product_id", product.getId());
        startActivity(i);
    }
}