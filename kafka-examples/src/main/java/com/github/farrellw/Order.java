package com.github.farrellw;

public class Order {
    public String price;
    public String item;

    Order(String price, String item){
        this.price = price;
        this.item = item;
    }

    // Creating toString
    @Override
    public String toString()
    {
        return "Organisation [price="
                + price
                + ", item="
                + item
                + "]";
    }
}
