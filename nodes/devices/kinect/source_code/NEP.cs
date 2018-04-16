using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;



class advertising
{
    public string topic { get; set; }
    public string mode { get; set; }
    public string node_name { get; set; }
}

class advertising_response
{
    public string topic { get; set; }
    public string port { get; set; }
}


class Client
{
    advertising a = new advertising();
    RequestSocket client;
    public Client(string IP, string port)
    {
        client = new RequestSocket("tcp://localhost:7000");
    }
    public void send_info(object obj)
    {
        string json = JsonConvert.SerializeObject(obj);
        this.client.SendFrame(json, false);
    }

    public advertising_response listen_info()
    {
        string msg = client.ReceiveFrameString();
        advertising_response response = JsonConvert.DeserializeObject<advertising_response>(msg);
        Console.WriteLine(msg);
        return response;
    }
}


class Publisher
{
    PublisherSocket pub;
    string topic;
    

    // TODO: add mode
    public Publisher(string topic, string msg_type, string network, string ip, string port)
    {
        this.pub = new PublisherSocket();
        this.topic = topic;
        pub.Options.SendHighWatermark = 1000;

        if (network == "direct")
        {
            string endpoint = "tcp://" + ip + ":" + port; //"tcp://localhost:9002"
            pub.Bind(endpoint);
        }
        else
        {
            Client client = new Client("localhost", "7000");
            advertising ad = new advertising();
            ad.topic = topic;
            ad.mode = "one2many";
            ad.node_name = "kinect";

            client.send_info(ad);
            advertising_response response = client.listen_info();
            topic = response.topic;
            port = response.port;
            string endpoint = "tcp://" + ip + ":" + port; //"tcp://localhost:9002";
            pub.Bind(endpoint);


        }

    }

    public void send_string(string value)
    {
        this.pub.SendFrame(this.topic + " " + value, false);
    }

    public void send_info(object obj)
    {
        string json = JsonConvert.SerializeObject(obj);
        this.pub.SendFrame(this.topic + " " + json, false);
    }

}