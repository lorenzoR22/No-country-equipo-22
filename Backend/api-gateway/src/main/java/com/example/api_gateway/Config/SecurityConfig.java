package com.example.api_gateway.Config;

import com.example.api_gateway.Security.JwtAuthenticationConverter;
import com.example.api_gateway.Security.JwtAuthenticationManager;
import com.example.api_gateway.Security.JwtUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.SecurityWebFiltersOrder;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;
import org.springframework.security.web.server.authentication.AuthenticationWebFilter;
import org.springframework.security.web.server.util.matcher.ServerWebExchangeMatchers;

@Configuration
@EnableWebFluxSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtUtils jwtUtils;

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        AuthenticationWebFilter authenticationWebFilter =
                new AuthenticationWebFilter(new JwtAuthenticationManager(jwtUtils));

        authenticationWebFilter.setServerAuthenticationConverter(new JwtAuthenticationConverter());
        authenticationWebFilter.setRequiresAuthenticationMatcher(ServerWebExchangeMatchers.anyExchange());

        return http
                .csrf(ServerHttpSecurity.CsrfSpec::disable)
                .authorizeExchange(exchange -> exchange
                        .pathMatchers("/api/auth/**").permitAll()
                        .anyExchange().authenticated()
                )
                .addFilterAt(authenticationWebFilter, SecurityWebFiltersOrder.AUTHENTICATION)
                .build();
    }
}
