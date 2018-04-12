package org.uiuc.cca.search.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController {

    @RequestMapping("/")
    public String index() {
        return "Greetings from Spring Boot!";
    }

}