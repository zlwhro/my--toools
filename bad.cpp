#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

int main()
{
    ofstream of; 
    of.open("/home/kali/my-tools/bad.txt", std::ios::out | std::ios::binary);
    vector<unsigned char> payload(1308,'A');
    vector<unsigned char> bad(256,0);
    bad[0] = 1;
    bad[10] = 1;
    bad[0x12] = 1;
    bad[0x1A] = 1;

    for(int i=0;i<256;++i)
        if(!bad[i])
            payload.push_back((unsigned char)i);
        else
            cout << "bad " << i << endl;


    of.write((char*)payload.data(), payload.size());
	of.close();

}